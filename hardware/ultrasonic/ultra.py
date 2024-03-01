from ultrasonic import get_ultra_distance

class Ultra:
    
    def __init__(self, mqtt_client, lookout_topic, threshold=5, count=0, memo=0):
        self.mqtt_client = mqtt_client
        self.lookout_topic = lookout_topic
        self.threshold = threshold
        self.count = count
        self.memo = memo
    
    def read_and_publish(self):
        dis = get_ultra_distance()
        decision = 0
        
        if (dis > self.threshold and self.memo > self.threshold) or (dis < self.threshold and self.memo < self.threshold):
            self.count += 1
        else:
            self.count = 0
            
        self.memo = dis
        
        if self.count >= 3:
            if dis < self.threshold and dis > 0:
                decision = 1
            else:
                decision = 0
            self.count = 0
        
        self.mqtt_client.publish(
            self.lookout_topic.encode(), str(decision).encode(), retain=True
        )
        
        print(f"dis = {dis} cm")
        print(f"Lookouts {self.lookout_topic}: published status {decision}")
    
            
            
        
        
        
        
        
