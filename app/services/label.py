from app.core.exceptions import (
    LabelAlreadyExistsException,
    LabelNotFoundException,
    NoteNotFoundException,
)
from app.models import Label
from app.repositories.label import LabelRepository
from app.repositories.note import NoteRepository
from app.schemas.label import LabelCreate, LabelUpdate


class LabelService:

    def __init__(
        self,
        repository: LabelRepository,
        note_repository: NoteRepository,
    ):
        self.repository = repository
        self.note_repository = note_repository

    async def _verify_note_ownership(self, note_id: int, user_id: int) -> None:
        note = await self.note_repository.get_by_id(note_id=note_id, user_id=user_id)
        if note is None:
            raise NoteNotFoundException(f"Note with ID {note_id} not found")

    async def get_all_labels(
        self,
        note_id: int,
        user_id: int,
    ) -> list[Label]:
        await self._verify_note_ownership(note_id=note_id, user_id=user_id)
        return await self.repository.get_all_by_note(note_id)

    async def create_label(
        self,
        note_id: int,
        label_data: LabelCreate,
        user_id: int,
    ) -> Label:
        await self._verify_note_ownership(note_id=note_id, user_id=user_id)

        existing_label = await self.repository.get_by_name_and_note(
            label_data.name,
            note_id,
        )

        if existing_label is not None:
            raise LabelAlreadyExistsException(
                f"Label '{label_data.name}' already exists"
            )

        label = Label(
            name=label_data.name,
            note_id=note_id,
        )

        return await self.repository.create(label)

    async def update_label(
        self,
        note_id: int,
        label_id: int,
        label_data: LabelUpdate,
        user_id: int,
    ) -> Label:
        await self._verify_note_ownership(note_id=note_id, user_id=user_id)

        label = await self.repository.get_by_id_and_note(
            label_id,
            note_id,
        )

        if label is None:
            raise LabelNotFoundException(
                f"Label with ID {label_id} not found in note {note_id}"
            )

        if "name" in label_data.model_fields_set:
            existing_label = await self.repository.get_by_name_and_note(
                label_data.name,
                note_id,
            )

            if existing_label is not None and existing_label.id != label.id:
                raise LabelAlreadyExistsException(
                    f"Label '{label_data.name}' already exists"
                )

            label.name = label_data.name

        return await self.repository.update(label)

    async def delete_label(
        self,
        note_id: int,
        label_id: int,
        user_id: int,
    ) -> None:
        await self._verify_note_ownership(note_id=note_id, user_id=user_id)

        label = await self.repository.get_by_id_and_note(
            label_id,
            note_id,
        )

        if label is None:
            raise LabelNotFoundException(
                f"Label with ID {label_id} not found in note {note_id}"
            )

        await self.repository.delete(label)