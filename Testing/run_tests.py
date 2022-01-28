import Loading.calc_indexes


def test_divergence():
    area = {
        'BROWN': 100,
        'POP': 1000,
        'Sub Areas': [
            {
                'BROWN': 40,
                'POP': 50
            },
            {
                'BROWN': 30,
                'POP': 100
            },
            {
                'BROWN': 10,
                'POP': 500
            },
            {
                'BROWN': 20,
                'POP': 200
            },
            {
                'BROWN': 0,
                'POP': 150
            }
        ]
    }
    print(Loading.calc_indexes.calc_divergence(area['Sub Areas'], area))
    print(Loading.calc_indexes.calc_iso(area['Sub Areas'], area))


test_divergence()
