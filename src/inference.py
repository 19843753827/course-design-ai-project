import cv2
import numpy as np
import torch
import torchvision.transforms as T

from model import DefectCNN
from dataset import ID2LABEL

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DefectPredictor:
    def __init__(self, weight_path):
        self.model = DefectCNN(num_classes=6).to(DEVICE)
        self.model.load_state_dict(torch.load(weight_path, map_location=DEVICE))
        self.model.eval()

        self.transform = T.Compose([
            T.ToPILImage(),
            T.Resize((200, 200)),
            T.ToTensor(),
            T.Normalize([0.5], [0.5])
        ])

    def predict_image(self, img_bytes):
        """
        :param img_bytes:二进制图片字节流（web上传拿到）
        :return dict: {pred_label_name,confidence,prob_list}
        """
        img_np = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(img_np, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("图片解析失败")

        tensor_img = self.transform(image).unsqueeze(0)  #增加batch维度 [1,1,200,200]
        tensor_img = tensor_img.to(DEVICE)

        with torch.no_grad():
            output = self.model(tensor_img)
            probs = torch.softmax(output, dim=1)[0].cpu().numpy()

        pred_idx = int(np.argmax(probs))
        pred_name = ID2LABEL[pred_idx]
        confidence = float(probs[pred_idx])

        return {
            "predict_index": pred_idx,
            "predict_class": pred_name,
            "confidence": round(confidence,4),
            "probabilities": probs.tolist()
        }


if __name__ == "__main__":
    #本地测试示例
    predictor = DefectPredictor("../models/defect_cnn.pth")
    with open(r"../data/samples/crazing_1.jpg", "rb") as f:
        byte_data = f.read()
    res = predictor.predict_image(byte_data)
    print("推理结果：", res)
