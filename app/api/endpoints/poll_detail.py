from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import getDb
from app.crud import poll_detail as poll_detail_crud
from app.schemas.poll_detail import PollDetailResponse, PollOptionDetail

router = APIRouter()


@router.get("/{poll_id}", response_model=PollDetailResponse)
def read_poll_detail(
    poll_id: int,
    db: Session = Depends(getDb),
):
    poll = poll_detail_crud.get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Poll not found",
        )

    options = poll_detail_crud.get_poll_options(db, poll_id)
    if len(options) != 2:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Poll detail requires exactly two options",
        )

    now = datetime.utcnow()
    is_ended = poll_detail_crud.is_poll_ended(poll, now)
    effective_status = "ENDED" if is_ended and poll.status == "ONGOING" else poll.status
    remaining_seconds = 0
    if poll.end_time is not None and not is_ended:
        remaining_seconds = max(int((poll.end_time - now).total_seconds()), 0)

    results_visible = True

    participant_count = poll_detail_crud.get_participant_count(db, poll_id)
    total_bet_credits = poll_detail_crud.get_total_bet_credits(db, poll_id)
    bet_credits_by_option = poll_detail_crud.get_bet_credits_by_option(db, poll_id)
    total_votes = sum(option.vote_count or 0 for option in options)

    option_details = []
    for option in options:
        vote_count = option.vote_count or 0
        vote_ratio = round((vote_count / total_votes) * 100, 2) if total_votes else 0.0
        option_details.append(
            PollOptionDetail(
                id=option.id,
                option_text=option.option_text,
                vote_count=vote_count,
                vote_ratio=vote_ratio,
                bet_credits=bet_credits_by_option.get(option.id, 0),
            )
        )

    winner_option_id = None
    is_draw = False
    if is_ended:
        first_count = options[0].vote_count or 0
        second_count = options[1].vote_count or 0
        if first_count == second_count:
            is_draw = True
        else:
            winner_option_id = options[0].id if first_count > second_count else options[1].id

    return PollDetailResponse(
        id=poll.id,
        title=poll.title,
        status=effective_status,
        end_time=poll.end_time,
        remaining_seconds=remaining_seconds,
        participant_count=participant_count,
        total_bet_credits=total_bet_credits,
        options=option_details,
        results_visible=results_visible,
        can_vote=not is_ended and poll.status == "ONGOING",
        can_bet=not is_ended and poll.status == "ONGOING",
        winner_option_id=winner_option_id,
        is_draw=is_draw,
    )
