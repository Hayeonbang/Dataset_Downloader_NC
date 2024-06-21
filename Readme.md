# Data Downloader for Youtube-Human Annotation Dataset
유튜브와 휴먼 어노테이션 데이터셋을 다운로드하기 위한 스크립트입니다. 

```setup
git clone https://github.com/Hayeonbang/nc-kaist_dataset_downloader.git
cd nc-kaist_dataset_downloader
pip install -r requirements.txt
```

## 주요 기능
- *dataset/Youtube_ytid.csv* 파일의 youtube id 목록을 사용하여 데이터 다운로드
    - 데이터 구성
        - 오디오 파일(.mp3)
        - 텍스트 파일(.json): 동영상 제목, 길이(초), 태그, 설명 
- 30분 이상의 오디오 파일을 10분 단위로 분할


## 데이터셋 설명
1. Youtube_Dataset 

    최종 발표 이후 데이터셋 품질 상승을 위해 피아노 솔로 필터 과정을 한 번 더 거쳤습니다. 최종 트랙의 개수는 5988 트랙이며, 유튜브에서 삭제된 비디오들은 다운로드되지 않을 수 있습니다.

2. Annotation_Dataset
   
    [데이터셋 다운로드](http://www.blablabla) 

## 사용 방법
1. 스크립트 실행:
```setup
python main.py
```
2. 스크립트는 각 Youtube ID에 대해 오디오 파일과 텍스트 데이터를 다운로드합니다.
3. 다운로드가 완료되면 폴더에 다음 디렉토리가 생성됩니다.
    - data/audio: 오디오 데이터
    - data/meta: 텍스트 데이터 파일
    - data/long_files: 30분 이상 오디오 데이터의 원본 파일 

