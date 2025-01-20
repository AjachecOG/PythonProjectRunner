def draw_background(screen, sky, ground, offset, sky_width, ground_width):
    sky_offset_factor = 0.10
    sky_offset = offset * sky_offset_factor
    start_sky = -(sky_offset % sky_width)
    for x in range(int(start_sky), 600 + sky_width, sky_width):
        screen.blit(sky, (x, 0))

    start_ground = -(offset % ground_width)
    for x in range(int(start_ground), 600 + ground_width, ground_width):
        screen.blit(ground, (x, 400))
