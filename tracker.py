import math

class Tracker:
    def __init__(self):
        # Nesnelerin merkez pozisyonlarını saklar
        self.center_points = {}
        # Benzersiz nesne kimliklerini tutar
        self.id_count = 0

    def update(self, objects_rect):
        # Güncellenen nesne kutuları ve kimlikleri
        objects_bbs_ids = []

        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2 # Nesnenin yatay merkezi
            cy = (y + y + h) // 2# Nesnenin dikey merkezi

            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:# Eğer nesne daha önce algılandıysa
                    self.center_points[id] = (cx, cy)# Nesnenin merkezi güncellenir
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            if not same_object_detected: # Yeni bir nesne algılandıysa
                self.center_points[self.id_count] = (cx, cy) # Yeni nesnenin merkezi kaydedilir
                objects_bbs_ids.append([x, y, w, h, self.id_count])  # Yeni kimlik atanır
                self.id_count += 1 # Kimlik sayacı artırılır

        # Kullanılmayan nesne kimliklerini temizle
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        self.center_points = new_center_points.copy()
        return objects_bbs_ids
