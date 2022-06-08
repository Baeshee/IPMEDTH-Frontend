from matplotlib import pyplot as plt
import pandas as pd

data = {
            "finger_thumb": {"THUMB_IP": {"x": 237, "y": 273}, "THUMB_CMC": {"x": 314, "y": 309}, "THUMB_MCP": {"x": 273, "y": 286}, "THUMB_TIP": {"x": 206, "y": 266}},
                        "finger_index": {"INDEX_FINGER_DIP": {"x": 272, "y": 141}, "INDEX_FINGER_MCP": {"x": 300, "y": 214}, "INDEX_FINGER_PIP": {"x": 281, "y": 169}, "INDEX_FINGER_TIP": {"x": 265, "y": 116}},
                        "finger_middle": {"MIDDLE_FINGER_DIP": {"x": 310, "y": 122}, "MIDDLE_FINGER_MCP": {"x": 326, "y": 205}, "MIDDLE_FINGER_PIP": {"x": 316, "y": 154}, "MIDDLE_FINGER_TIP": {"x": 306, "y": 94}},
                        "finger_ring": {"PINKY_DIP": {"x": 402, "y": 163}, "PINKY_MCP": {"x": 378, "y": 220}, "PINKY_PIP": {"x": 393, "y": 186}, "PINKY_TIP": {"x": 408, "y": 140}},
                        "finger_pink": {"RING_FINGER_DIP": {"x": 351, "y": 127}, "RING_FINGER_MCP": {"x": 352, "y": 208}, "RING_FINGER_PIP": {"x": 352, "y": 159}, "RING_FINGER_TIP": {"x": 349, "y": 99}},
                        "wrist": {"WRIST": {"x": 359, "y": 319}},
        }

# data = {
#     "finger_thumb": {"THUMB_IP": {"x": 312, "y": 278}, "THUMB_CMC": {"x": 267, "y": 292}, "THUMB_MCP": {"x": 286, "y": 285}, "THUMB_TIP": {"x": 226, "y": 303}},
#     "finger_index": {"INDEX_FINGER_DIP": {"x": 304, "y": 266}, "INDEX_FINGER_MCP": {"x": 241, "y": 291}, "INDEX_FINGER_PIP": {"x": 262, "y": 278}, "INDEX_FINGER_TIP": {"x": 216, "y": 302}},
#     "finger_middle": {"MIDDLE_FINGER_DIP": {"x": 296, "y": 260}, "MIDDLE_FINGER_MCP": {"x": 231, "y": 288}, "MIDDLE_FINGER_PIP": {"x": 253, "y": 273}, "MIDDLE_FINGER_TIP": {"x": 217, "y": 287}},
#     "finger_ring": {"PINKY_DIP": {"x": 341, "y": 294}, "PINKY_MCP": {"x": 294, "y": 300}, "PINKY_PIP": {"x": 314, "y": 296}, "PINKY_TIP": {"x": 368, "y": 277}},
#     "finger_pink": {"RING_FINGER_DIP": {"x": 292, "y": 261}, "RING_FINGER_MCP": {"x": 234, "y": 278}, "RING_FINGER_PIP": {"x": 255, "y": 269}, "RING_FINGER_TIP": {"x": 277, "y": 306}},
#     "wrist": {"WRIST": {"x": 251, "y": 299}},
# }

colors = ["#ffe5b4", "#804080", "#ffcc00", "#30ff30", "#1565c0", '#ff3030']

finger_thumb = pd.DataFrame(data['finger_thumb'])
finger_index = pd.DataFrame(data['finger_index'])
finger_middle = pd.DataFrame(data['finger_middle'])
finger_ring = pd.DataFrame(data['finger_ring'])
finger_pink = pd.DataFrame(data['finger_pink'])
wrist = pd.DataFrame(data['wrist'])

df = pd.concat([finger_thumb, finger_index, finger_middle, finger_ring, finger_pink, wrist], axis=1)
df = df.T

fig, ax = plt.subplots()

padding = 50
plt.axis([df['x'].min() - padding, df['x'].max() + padding, df['y'].min() - padding, df['y'].max() + padding])

for k, v in df.iterrows():
    if "THUMB" in k:
        ax.scatter(v[0], v[1], color=colors[0])
        
    if "INDEX" in k:
        ax.scatter(v[0], v[1], color=colors[1])
        
    if "MIDDLE" in k:
        ax.scatter(v[0], v[1], color=colors[2])
        
    if "RING" in k:
        ax.scatter(v[0], v[1], color=colors[3])
        
    if "PINKY" in k:
        ax.scatter(v[0], v[1], color=colors[4])
    
    if "WRIST" in k:
        ax.scatter(v[0], v[1], color=colors[5])
        
    ax.annotate(k, v,
                xytext=(-10,10), 
                textcoords='offset points',
                size=6, 
                color='darkslategrey')

plt.show()