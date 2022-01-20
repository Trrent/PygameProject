import ctypes


user32 = ctypes.windll.user32
WIDTH, HEIGHT = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

FPS = 60
skeletons1 = (
    (17, 7), (27, 7), (36, 4), (48, 2), (47, 8), (55, 6), (60, 4), (73, 1), (74, 3), (81, 3), (89, 1), 
    (86, 7), (89, 5), (88, 3), (91, 3), (93, 8), (113, 2), (113, 4), (105, 5), (102, 9))