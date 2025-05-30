def get_chosung_range(chosung: str):
    chosung_range = {
        'ㄱ': ('가', '깋'),
        'ㄴ': ('나', '닣'),
        'ㄷ': ('다', '딯'),
        'ㄹ': ('라', '맇'),
        'ㅁ': ('마', '밓'),
        'ㅂ': ('바', '빟'),
        'ㅅ': ('사', '싷'),
        'ㅇ': ('아', '잏'),
        'ㅈ': ('자', '잏'), 
        'ㅊ': ('차', '칳'),
        'ㅋ': ('카', '킿'),
        'ㅌ': ('타', '팋'),
        'ㅍ': ('파', '핗'),
        'ㅎ': ('하', '힣')
    }
    return chosung_range.get(chosung)
