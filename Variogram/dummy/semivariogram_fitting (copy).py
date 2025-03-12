import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pykrige.ok import OrdinaryKriging
import warnings
warnings.filterwarnings('ignore')

# Load the data
data = pd.read_csv('Stacking_results_ANDMC1518_RES.csv')

# Extract the 'depth_input' and 'RES' columns
depth = data['depth_input'].values
ze = np.zeros_like(depth)  # 2D 좌표를 위해 y 좌표를 0으로 설정
coords = np.column_stack((depth, ze))
values = data['RES'].values

# 사용할 세미베리오그램 모델 설정 (예: spherical)
model_name = 'gaussian'

# 플롯 생성
plt.figure(figsize=(10, 6))

try:
    # Ordinary Kriging 객체 생성 (enable_statistics=True로 실험적 세미베리오그램 계산 활성화)
    OK = OrdinaryKriging(
        coords[:, 0],  # x 좌표 (depth)
        coords[:, 1],  # y 좌표 (ze)
        values,        # 값 (RES)
        variogram_model=model_name,
        nlags=100,      # lag 수
        verbose=False,
        enable_plotting=False,
        enable_statistics=True  # 실험적 세미베리오그램 계산 활성화
    )

    # 실험적 세미베리오그램 추출 (lags와 semivariance 사용)
    lags = OK.lags
    experimental = OK.semivariance

    # 이론적 세미베리오그램 계산
    theoretical = OK.variogram_function(OK.variogram_model_parameters, lags)

    # 피팅된 모델 플롯
    plt.plot(lags, experimental, 'o', label=f'{model_name} - Experimental')
    plt.plot(lags, theoretical, '-', label=f'{model_name} - Theoretical')
    print(f"Model {model_name} fitted successfully.")
except Exception as e:
    print(f"Error with model {model_name}: {e}")

plt.title(f'Semivariogram - {model_name}')
plt.xlabel('Lag Distance')
plt.ylabel('Semivariance')
plt.legend()
plt.grid(True)
plt.show()