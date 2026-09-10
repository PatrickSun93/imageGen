#!/bin/bash
# SDXL 人物 LoRA 训练（Apple Silicon / MPS）
# 用法: ./train.sh   日志在 lora_training/train.log
ROOT=/Volumes/externalssd/devitems/learning/imageGen
LT="$ROOT/lora_training"
cd "$LT/sd-scripts" || exit 1

export PYTORCH_ENABLE_MPS_FALLBACK=1        # 训练里有算子 MPS 没实现，回落 CPU 而不是崩
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 # 不让 MPS 分配器过早 OOM

exec ./venv/bin/python sdxl_train_network.py \
  --pretrained_model_name_or_path="$ROOT/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors" \
  --dataset_config="$LT/dataset_config.toml" \
  --output_dir="$LT/output" \
  --output_name="son_ohwx_v2" \
  --save_model_as=safetensors \
  --network_module=networks.lora \
  --network_dim=16 \
  --network_alpha=8 \
  --learning_rate=1e-4 \
  --unet_lr=1e-4 \
  --text_encoder_lr=0 \
  --network_train_unet_only \
  --lr_scheduler=cosine \
  --lr_warmup_steps=50 \
  --optimizer_type=AdamW \
  --max_train_steps=1800 \
  --save_every_n_steps=400 \
  --mixed_precision=no \
  --save_precision=fp16 \
  --gradient_checkpointing \
  --cache_latents \
  --max_data_loader_n_workers=0 \
  --seed=42 \
  --logging_dir="$LT/logs" \
  --log_prefix=son_lora
