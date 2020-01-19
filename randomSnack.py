import random
def randomSnack(rows, item, interval):
    positions = item.body

    while True:
        x = random.randrange(rows) * interval
        y = random.randrange(rows) * interval
        if len(list(filter(lambda z: z.pos == (x + 1, y + 1), positions))) > 0:
            continue
        else:
            break

    return (x + 1, y + 1)