import ctypes


user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

FPS = 60
skeletonsCoords = [
    (
    (17, 7), (27, 7), (36, 4), (48, 2), (47, 8), (55, 6), (60, 4), (73, 1), (74, 3), (81, 3), (89, 1), 
    (89, 5), (88, 3), (91, 3), (93, 8), (113, 2), (113, 4), (105, 5), (102, 9)
    ), (
       (11, 9), (25, 1), (25, 4), (33, 1), (26, 8), (46, 6), (56, 4), (64, 10), (84, 6), (95, 3), (96, 3), 
       (97, 3), (90, 10), (90, 8), (96, 6), (101, 7), (106, 5), (112, 5), (113, 5)
    ), (
       (4, 4), (10, 6), (23, 5), (33, 6), (35, 6), (39, 6), (43, 6), (58, 5), (57, 5), (67, 10), (97, 2))]