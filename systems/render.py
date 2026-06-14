def render_pet(pet, painter):
    if not pet.animation.frames:
        return

    pixmap = pet.animation.frames[pet.animation.frame_index]

    painter.save()

    # Move origin to center of window
    painter.translate(pet.width() / 2, pet.height() / 2)

    # Apply slight rotation
    rotation = 0

    # only apply tilt when walking
    if pet.state == "walk":
        if pet.movement.dy == -1:
            rotation = 8
        elif pet.movement.dy == 1:
            rotation = -8

        if pet.facing == "right":
            rotation = -rotation

    painter.rotate(rotation)

    # Mirror if facing right
    if pet.facing == "right":
        painter.scale(-1, 1)

    # Draw sprite centered at origin
    painter.drawPixmap(
        -pixmap.width() // 2,
        -pixmap.height() // 2,
        pixmap
    )

    painter.restore()