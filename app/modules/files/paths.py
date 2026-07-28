class FilePath:

    def generate(
        self,
        *,
        owner_type: str,
        owner_id: str,
        category: str,
        filename: str,
    ) -> str:

        return (
            f"{owner_type}/{owner_id}/{category}/{filename}"
        )