package com.example.myapplication;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import java.io.File;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {

    private static final int IMAGE_REQUEST = 1;
    private Uri imageUri;
    private ImageView imageView;
    private TextView resultText;
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = findViewById(R.id.imageView);
        Button selectImageBtn = findViewById(R.id.selectImageBtn);
        Button uploadBtn = findViewById(R.id.uploadBtn);
        resultText = findViewById(R.id.resultTextView);

        // Initialize Retrofit instance via ApiService interface
        apiService = RetrofitClient.getRetrofitInstance().create(ApiService.class);

        selectImageBtn.setOnClickListener(v -> openGallery());
        uploadBtn.setOnClickListener(v -> {
            if (imageUri != null) uploadImage();
            else Toast.makeText(this, "Select image first", Toast.LENGTH_SHORT).show();
        });
    }

    // Open the gallery to select an image
    private void openGallery() {
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        startActivityForResult(intent, IMAGE_REQUEST);
    }

    // Handle result after image selection from gallery
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == IMAGE_REQUEST && resultCode == RESULT_OK && data != null) {
            imageUri = data.getData();
            imageView.setImageURI(imageUri);
        }
    }

    @SuppressLint("SetTextI18n")
    private void uploadImage() {
        try {
            // Convert Uri to File
            File file = FileUtil.from(this, imageUri);
            RequestBody reqFile = RequestBody.create(MediaType.parse("image/*"), file);
            MultipartBody.Part body = MultipartBody.Part.createFormData("file", file.getName(), reqFile);

            // Send image to server using Retrofit
            Call<ResponseBody> call = apiService.uploadImage(body);
            call.enqueue(new Callback<ResponseBody>() {
                @Override
                public void onResponse(@NonNull Call<ResponseBody> call, @NonNull Response<ResponseBody> response) {
                    try {
                        if (response.isSuccessful() && response.body() != null) {
                            String result = response.body().string();
                            resultText.setText("Result: " + result);
                        } else {
                            resultText.setText("Failed to get prediction");
                        }
                    } catch (Exception e) {
                        resultText.setText("Error parsing result");
                    }
                }

                @Override
                public void onFailure(@NonNull Call<ResponseBody> call, @NonNull Throwable t) {
                    resultText.setText("Failed: " + t.getMessage());
                }
            });
        } catch (Exception e) {
            resultText.setText("Upload error: " + e.getMessage());
        }
    }
}