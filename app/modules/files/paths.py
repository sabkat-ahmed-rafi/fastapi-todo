class FilePath:

    def user_avatar(
        self,
        user_id,
        filename
    ):

        return (
            f"users/{user_id}/avatar/{filename}"
        )


    def product_image(
        self,
        product_id,
        filename
    ):

        return (
            f"products/{product_id}/images/{filename}"
        )