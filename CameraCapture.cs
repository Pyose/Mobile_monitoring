using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;
using Unity.Barracuda;
using UnityEngine.Networking;  // UnityWebRequestを使うために必要
using Newtonsoft.Json.Linq;

public class CameraCapture : MonoBehaviour
{
    private WebCamTexture webcamTexture;
    public RawImage cameraDisplay;    // カメラ映像を表示するRawImage
    public RawImage photoPreview;     // 撮影した画像を表示するRawImage
    [SerializeField] public Button captureButton;      //撮影用ボタン
    [SerializeField] public Button backButton;         //戻るボタン
    [SerializeField] public Button nextButton;         // 新しいアクション用のボタン
    public GameObject boundingBoxPrefab; // バウンディングボックスのプレハブ

    private byte[] imageData;

    void Start()
    {
        Debug.Log(Application.persistentDataPath + "/photo.png");
        if (WebCamTexture.devices.Length > 0)
        {
            WebCamDevice device = WebCamTexture.devices[0];
            webcamTexture = new WebCamTexture(device.name);

            cameraDisplay.texture = webcamTexture;
            cameraDisplay.material.mainTexture = webcamTexture;

            webcamTexture.Play();
        }
        else
        {
            Debug.LogError("カメラデバイスが見つかりません。");
        }

        // 撮影後のプレビュー画像とボタンを非表示にしておく
        photoPreview.gameObject.SetActive(false);
        backButton.gameObject.SetActive(false);
        nextButton.gameObject.SetActive(false);
        boundingBoxPrefab.gameObject.SetActive(false);

        // ボタンにクリックイベントを設定
        nextButton.onClick.AddListener(OnClick);
        captureButton.onClick.AddListener(CapturePhoto);
        backButton.onClick.AddListener(ReturnToCameraView);
        
        
    }

    void update()
    {
        webcamTexture.Play();
    }

    public void CapturePhoto()
    {
        if (webcamTexture != null && webcamTexture.isPlaying)
        {
            // WebCamTextureから現在のフレームを取得
            Texture2D photo = new Texture2D(webcamTexture.width, webcamTexture.height);
            photo.SetPixels(webcamTexture.GetPixels());
            photo.Apply();

            // PNG形式でバイト配列に変換して保存（省略可能）
            imageData = photo.EncodeToPNG();
            //System.IO.File.WriteAllBytes(Application.persistentDataPath + "/photo.png", imageData);
            //Debug.Log("写真が保存されました: " + Application.persistentDataPath + "/photo.png");

            // 撮影した画像をプレビューに表示
            photoPreview.texture = photo;
            photoPreview.gameObject.SetActive(true);  // プレビューを表示
            backButton.gameObject.SetActive(true);
            // 次のアクション用のボタンを表示
            nextButton.gameObject.SetActive(true);
        }
    }

    public void ReturnToCameraView()
    {
        // カメラ映像を表示し、プレビュー画面を非表示にする
        cameraDisplay.gameObject.SetActive(true);
        photoPreview.gameObject.SetActive(false);
        captureButton.gameObject.SetActive(true);
        backButton.gameObject.SetActive(false);
        nextButton.gameObject.SetActive(false);
    }

    public void OnClick()
    {
        Debug.Log("pushing.");
        if (imageData != null)
        {
            StartCoroutine(SendImageToServer(imageData));
        }
        else
        {
            Debug.LogError("画像データがありません。");
        }
        Debug.Log("pushed.");
    }

    IEnumerator SendImageToServer(byte[] imageData)
    {
        string url = "http://10.0.0.1:5000/upload";

        UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(imageData);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "image/png");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("リクエスト成功");

            // 画像をテクスチャに変換して表示
            Texture2D receivedTexture = new Texture2D(2, 2);
            receivedTexture.LoadImage(request.downloadHandler.data);

            // 画像を表示するRawImageに適用
            photoPreview.texture = receivedTexture;
        }
        else if (request.result == UnityWebRequest.Result.ConnectionError)
        {
            Debug.LogError("接続エラー: サーバーに接続できませんでした。");
        }
        else if (request.result == UnityWebRequest.Result.ProtocolError)
        {
            Debug.LogError("プロトコルエラー: サーバーがエラーを返しました。");
        }
        else if (request.result == UnityWebRequest.Result.DataProcessingError)
        {
            Debug.LogError("データ処理エラー: データ処理中にエラーが発生しました。");
        }
        else
        {
            Debug.LogError("リクエスト失敗: " + request.error);
        }
    }

}



