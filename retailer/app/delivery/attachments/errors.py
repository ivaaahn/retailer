from app.base.errors import NotFoundError


class AttachmentNotFound(NotFoundError):
    def __init__(self, key: str):
        super().__init__(
            description=f"Attachment {key} not found",
            data={
                "key": key,
            },
        )
