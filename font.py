import pygame
pygame.font.init()
available_fonts = pygame.font.get_fonts()
print("사용 가능한 폰트 중 'nanum' 또는 'gothic' 포함된 폰트:")
for font_name in available_fonts:
    if 'nanum' in font_name.lower() or 'gothic' in font_name.lower():
        print(font_name)
# print("\n전체 사용 가능 폰트 목록:")
# print(available_fonts) # 필요시 전체 목록 확인
pygame.font.quit()
