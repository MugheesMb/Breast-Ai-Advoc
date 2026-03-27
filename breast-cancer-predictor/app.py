import gradio as gr
import torch
import torch.nn as nn
import pickle
import numpy as np

# ── Model definition (must match the training notebook exactly) ──────────────
class ANN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.network(x)


# ── Load model and scaler ─────────────────────────────────────────────────────
model = ANN(input_dim=30)
model.load_state_dict(torch.load('breast_cancer_model.pth', map_location='cpu'))
model.eval()

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)


# ── Prediction function ───────────────────────────────────────────────────────
def predict(
    radius_mean, texture_mean, perimeter_mean, area_mean,
    smoothness_mean, compactness_mean, concavity_mean, concave_points_mean,
    symmetry_mean, fractal_dimension_mean,
    radius_se, texture_se, perimeter_se, area_se,
    smoothness_se, compactness_se, concavity_se, concave_points_se,
    symmetry_se, fractal_dimension_se,
    radius_worst, texture_worst, perimeter_worst, area_worst,
    smoothness_worst, compactness_worst, concavity_worst, concave_points_worst,
    symmetry_worst, fractal_dimension_worst
):
    features = np.array([[
        radius_mean, texture_mean, perimeter_mean, area_mean,
        smoothness_mean, compactness_mean, concavity_mean, concave_points_mean,
        symmetry_mean, fractal_dimension_mean,
        radius_se, texture_se, perimeter_se, area_se,
        smoothness_se, compactness_se, concavity_se, concave_points_se,
        symmetry_se, fractal_dimension_se,
        radius_worst, texture_worst, perimeter_worst, area_worst,
        smoothness_worst, compactness_worst, concavity_worst, concave_points_worst,
        symmetry_worst, fractal_dimension_worst
    ]])

    scaled   = scaler.transform(features)
    tensor   = torch.tensor(scaled, dtype=torch.float32)

    with torch.no_grad():
        prob = model(tensor).item()

    label      = "🔴 Malignant (Cancerous)" if prob >= 0.5 else "🟢 Benign (Non-cancerous)"
    confidence = prob if prob >= 0.5 else 1 - prob
    return f"{label}\nConfidence: {confidence:.1%}"


# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(title="Breast Cancer Prediction") as demo:
    gr.Markdown("# 🔬 Breast Cancer Prediction")
    gr.Markdown(
        "Enter tumor measurements to predict whether it is **Malignant** or **Benign**. "
        "All 30 features from the Wisconsin Breast Cancer Dataset are used."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Mean Features")
            radius_mean            = gr.Number(label="Radius Mean",             value=14.13)
            texture_mean           = gr.Number(label="Texture Mean",            value=19.27)
            perimeter_mean         = gr.Number(label="Perimeter Mean",          value=91.97)
            area_mean              = gr.Number(label="Area Mean",               value=654.9)
            smoothness_mean        = gr.Number(label="Smoothness Mean",         value=0.096)
            compactness_mean       = gr.Number(label="Compactness Mean",        value=0.104)
            concavity_mean         = gr.Number(label="Concavity Mean",          value=0.089)
            concave_points_mean    = gr.Number(label="Concave Points Mean",     value=0.049)
            symmetry_mean          = gr.Number(label="Symmetry Mean",           value=0.181)
            fractal_dimension_mean = gr.Number(label="Fractal Dimension Mean",  value=0.063)

        with gr.Column():
            gr.Markdown("### Standard Error Features")
            radius_se            = gr.Number(label="Radius SE",            value=0.405)
            texture_se           = gr.Number(label="Texture SE",           value=1.216)
            perimeter_se         = gr.Number(label="Perimeter SE",         value=2.866)
            area_se              = gr.Number(label="Area SE",               value=40.34)
            smoothness_se        = gr.Number(label="Smoothness SE",        value=0.007)
            compactness_se       = gr.Number(label="Compactness SE",       value=0.025)
            concavity_se         = gr.Number(label="Concavity SE",         value=0.032)
            concave_points_se    = gr.Number(label="Concave Points SE",    value=0.012)
            symmetry_se          = gr.Number(label="Symmetry SE",          value=0.020)
            fractal_dimension_se = gr.Number(label="Fractal Dimension SE", value=0.004)

        with gr.Column():
            gr.Markdown("### Worst Features")
            radius_worst            = gr.Number(label="Radius Worst",            value=16.27)
            texture_worst           = gr.Number(label="Texture Worst",           value=25.68)
            perimeter_worst         = gr.Number(label="Perimeter Worst",         value=107.3)
            area_worst              = gr.Number(label="Area Worst",              value=880.6)
            smoothness_worst        = gr.Number(label="Smoothness Worst",        value=0.132)
            compactness_worst       = gr.Number(label="Compactness Worst",       value=0.253)
            concavity_worst         = gr.Number(label="Concavity Worst",         value=0.272)
            concave_points_worst    = gr.Number(label="Concave Points Worst",    value=0.115)
            symmetry_worst          = gr.Number(label="Symmetry Worst",          value=0.290)
            fractal_dimension_worst = gr.Number(label="Fractal Dimension Worst", value=0.084)

    predict_btn = gr.Button("🔍 Predict", variant="primary")
    output      = gr.Textbox(label="Prediction Result", lines=2)

    predict_btn.click(
        fn=predict,
        inputs=[
            radius_mean, texture_mean, perimeter_mean, area_mean,
            smoothness_mean, compactness_mean, concavity_mean, concave_points_mean,
            symmetry_mean, fractal_dimension_mean,
            radius_se, texture_se, perimeter_se, area_se,
            smoothness_se, compactness_se, concavity_se, concave_points_se,
            symmetry_se, fractal_dimension_se,
            radius_worst, texture_worst, perimeter_worst, area_worst,
            smoothness_worst, compactness_worst, concavity_worst, concave_points_worst,
            symmetry_worst, fractal_dimension_worst
        ],
        outputs=output
    )

    gr.Markdown(
        "> ⚠️ This tool is for educational purposes only. "
        "Always consult a qualified medical professional for diagnosis."
    )

demo.launch()
