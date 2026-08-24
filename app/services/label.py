from app.core.exceptions import (
    LabelAlreadyExistsException,
    LabelNotFoundException,
)
from app.models import Label
from app.repositories.label import LabelRepository
from app.schemas.label import LabelCreate, LabelUpdate


class LabelService:

    def __init__(self, repository: LabelRepository):
        self.repository = repository

    async def get_all_labels(
        self,
        note_id: int,
    ) -> list[Label]:

        return await self.repository.get_all_by_note(note_id)

    async def create_label(
        self,
        note_id: int,
        label_data: LabelCreate,
    ) -> Label:

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
    ) -> Label:

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

            if (
                existing_label is not None
                and existing_label.id != label.id
            ):
                raise LabelAlreadyExistsException(
                    f"Label '{label_data.name}' already exists"
                )

            label.name = label_data.name

        return await self.repository.update(label)

    async def delete_label(
        self,
        note_id: int,
        label_id: int,
    ) -> None:

        label = await self.repository.get_by_id_and_note(
            label_id,
            note_id,
        )

        if label is None:
            raise LabelNotFoundException(
                f"Label with ID {label_id} not found in note {note_id}"
            )

        await self.repository.delete(label)