# Django 專案使用說明 - Render 部署版

## 專案簡介
專案配置為無資料庫模式，主要用於展示靜態內容和 API 服務。該專案已經配置了 CORS 支援和 Django REST Framework，適合作為前後端分離專案的後端服務，後面有介紹資料庫的佈署。

## 結構
```
django-test/
├── app/                 # 主應用目錄
│   ├── templates/       # 模板檔案
│   ├── static/          # 靜態檔案（CSS、JS、圖片等）
│   ├── views.py         # 視圖函數
│   ├── models.py        # 資料模型（當前專案未使用資料庫）
│   └── forms.py         # 表單定義
├── django_test/         # 專案配置目錄
│   ├── settings.py      # 專案設定
│   ├── urls.py          # URL路由配置
│   └── wsgi.py          # WSGI配置
├── env/                 # 虛擬環境目錄
├── static/              # 收集的靜態檔案
├── requirements.txt     # 專案依賴
├── manage.py            # Django管理腳本
```

## 環境要求
- Python 3.9+
- Django 5.2
- PostgreSQL（雲端資料庫）
- 其他依賴見 `requirements.txt`

## 重要依賴套件
```
asgiref==3.8.1
colorama==0.4.6
dj-database-url==2.3.0      # 重要：雲端資料庫連接
Django==5.2
django-cors-headers==4.7.0  # 重要：CORS 支援
djangorestframework==3.16.0 # 重要：REST API
gunicorn==23.0.0            # 重要：WSGI 伺服器
psycopg2-binary==2.9.10     # 重要：PostgreSQL 驅動
whitenoise==6.9.0           # 重要：靜態檔案服務
```

## 安裝和設置

### 1. 複製專案
```bash
git clone <your-repository-url>
cd django-test
```

### 2. 建立虛擬環境（如果尚未建立）
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. 升級 pip 並安裝依賴
```bash
# 升級 pip
python -m pip install --upgrade pip

# 安裝依賴
pip install -r requirements.txt
```

### 4. 生成 requirements.txt（開發時使用）
```bash
# 啟動虛擬環境
env\Scripts\activate

# 收集靜態檔案
python manage.py collectstatic --noinput

# 生成依賴清單
pip freeze > requirements.txt
```

**注意**：如果遇到 UTF-8 編碼問題，可以在 VS Code 中轉換編碼方式。

### 4. 環境變數設置
在生產環境中，需要設置以下環境變數：
```bash
# Windows PowerShell
$env:SECRET_KEY = "your-secret-key-here"

# Windows CMD
set SECRET_KEY=your-secret-key-here

# macOS/Linux
export SECRET_KEY=your-secret-key-here
```

## 本地開發

### 啟動開發伺服器
```bash
# 啟動虛擬環境
env\Scripts\activate

# 啟動開發伺服器
python manage.py runserver
```

訪問 `http://127.0.0.1:8000/` 即可查看專案主頁。

### 收集靜態檔案
```bash
python manage.py collectstatic
```

## 專案特點

### 1. 無資料庫配置
- 專案配置為無資料庫模式，`DATABASES = {}`
- 禁用了資料庫相關的 Django 應用
- 不需要執行資料庫遷移

### 2. 靜態檔案處理
- 使用 WhiteNoise 中間件處理靜態檔案
- 配置了壓縮和快取優化
- 適合部署到 Render 等雲端平台

### 3. CORS 支援
- 已配置 `django-cors-headers`
- 當前設置允許來自 `https://sc2-myproject.onrender.com` 的請求
- 可根據需要修改 `CORS_ALLOWED_ORIGINS`

### 4. REST API 支援
- 整合了 Django REST Framework
- 可以輕鬆添加 API 端點

## 開發指南

### 添加新的視圖
1. 在 `app/views.py` 中添加新的視圖函數
2. 在 `django_test/urls.py` 中添加對應的 URL 路由

### 添加 API 端點
```python
# app/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_example(request):
    data = {'message': 'Hello from API'}
    return Response(data)
```

### 添加靜態檔案
1. 將檔案放入 `app/static/app/` 目錄
2. 執行 `python manage.py collectstatic` 收集靜態檔案

### 修改模板
- 模板檔案位於 `app/templates/app/` 目錄
- 使用 Django 模板語法

## Render 雲端部署配置(有資料庫)

### Settings.py 關鍵設定
```python
import os
import dj_database_url

# 安全設定
SECRET_KEY = os.environ.get('SECRET_KEY')  # 從環境變數獲取密鑰
DEBUG = False  # 生產環境關閉調試模式
ALLOWED_HOSTS = ['.onrender.com']  # Render 固定設定
APPEND_SLASH = True  # 固定設定

# CORS 設定
CORS_ALLOWED_ORIGINS = ["django-test-dqc9.onrender.com"]  # 你的雲端網址

# 中間件設定
MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

# 資料庫設定（支援 PostgreSQL 雲端資料庫）
DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}
```

### Render 部署步驟

#### 1. 準備專案
確保你的專案已推送到 GitHub 並包含以下檔案：
- `requirements.txt`
- `manage.py`
- 完整的 Django 專案結構

#### 2. 在 Render 建立 Web Service
1. 登入 [Render](https://render.com/)
2. 點擊 "New" → "Web Service"
3. 連接你的 GitHub 倉庫
4. 選擇你的 Django 專案

#### 3. 設定 Build 和 Start 命令
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python manage.py migrate && gunicorn [django專案資料夾名].wsgi:application`

例如：`python manage.py migrate && gunicorn django_test.wsgi:application`

#### 4. 設定環境變數
在 Render 的 Environment Variables 中設定：
- `SECRET_KEY`: 你的 Django 密鑰
- `DATABASE_URL`: PostgreSQL 資料庫連接字串（如果使用）

#### 5. 建立 PostgreSQL 資料庫（可選）
1. 在 Render 建立 PostgreSQL 資料庫
2. 複製 Database URL
3. 在 Web Service 環境變數中設定 `DATABASE_URL`

### 重要提醒
- **免費方案限制**：網站會在閒置時進入休眠狀態
- **24小時運行**：需要升級至付費方案
- **資料庫期限**：免費 PostgreSQL 資料庫約一個月後會自動清空
- **SECRET_KEY 安全**：切勿將密鑰上傳至 GitHub，使用環境變數

## 故障排除

### 常見問題
1. **靜態檔案不顯示**：執行 `python manage.py collectstatic --noinput`
2. **CORS 錯誤**：檢查 `CORS_ALLOWED_ORIGINS` 設置，確保包含正確的雲端網址
3. **SECRET_KEY 錯誤**：確保在 Render 環境變數中設置了 SECRET_KEY
4. **資料庫連接失敗**：檢查 `DATABASE_URL` 環境變數是否正確設定
5. **UTF-8 編碼問題**：在 VS Code 中轉換檔案編碼方式

### 本地開發模式
如果需要在本地開發，可以建立 `.env` 檔案或暫時修改 `settings.py`：
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
SECRET_KEY = 'your-local-secret-key'
```

### Render 部署檢查清單
- [ ] requirements.txt 已生成並包含所有依賴
- [ ] SECRET_KEY 已設定在環境變數
- [ ] CORS_ALLOWED_ORIGINS 包含正確的雲端網址
- [ ] Build Command 和 Start Command 設定正確
- [ ] 靜態檔案已收集（collectstatic）
- [ ] 資料庫遷移在 Start Command 中執行

## 專案依賴

### 核心依賴套件
- **Django 5.2**: Web 框架
- **djangorestframework 3.16.0**: REST API 支援
- **django-cors-headers 4.7.0**: CORS 跨域支援
- **dj-database-url 2.3.0**: 雲端資料庫連接
- **gunicorn 23.0.0**: WSGI 伺服器
- **psycopg2-binary 2.9.10**: PostgreSQL 資料庫驅動
- **whitenoise 6.9.0**: 靜態檔案服務

### 輔助套件
- **python-decouple 3.8**: 環境變數管理
- **pytest 8.3.5**: 測試框架
- **mysqlclient 2.2.7**: MySQL 支援（可選）

## 費用與限制

### 免費方案
- **Web Service**: 網站閒置時會休眠
- **PostgreSQL**: 約一個月後自動清空資料
- **靜態檔案**: 使用 WhiteNoise 免費服務

## 安全注意事項

1. **SECRET_KEY 管理**
   - 絕對不要將 SECRET_KEY 上傳至 GitHub
   - 如果不小心洩漏，立即重新生成新的密鑰
   - 使用環境變數存儲敏感資訊

2. **CORS 設定**
   - 只允許信任的域名存取 API
   - 定期檢查 CORS 設定是否正確

3. **資料庫安全**
   - 使用強密碼
   - 定期備份重要資料
   - 監控資料庫存取日誌

## 聯絡資訊
如有問題或建議，請聯絡專案維護者。