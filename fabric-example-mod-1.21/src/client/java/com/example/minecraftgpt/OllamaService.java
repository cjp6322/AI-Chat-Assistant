package com.example.minecraftgpt;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpClient.Version;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

public class OllamaService {
    private static final OllamaService INSTANCE = new OllamaService();

    private static final String ENDPOINT = "http://localhost:8000/chat";

    // force HTTP/1.1 (no h2c upgrade)
    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .version(Version.HTTP_1_1)
            .build();

    private OllamaService() {}

    public static OllamaService getInstance() {
        return INSTANCE;
    }

    public String ask(String question) throws IOException, InterruptedException {
        // Build the JSON payload
        JsonObject payload = new JsonObject();
        JsonArray messages = new JsonArray();
        JsonObject msg = new JsonObject();
        msg.addProperty("role", "user");
        msg.addProperty("content", question);
        messages.add(msg);
        payload.add("messages", messages);

        String jsonPayload = new Gson().toJson(payload);
        System.out.println(">> JSON-PAYLOAD: " + jsonPayload);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(ENDPOINT))
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                .build();

        HttpResponse<String> response = CLIENT
                .send(request, HttpResponse.BodyHandlers.ofString());

        JsonObject result = JsonParser.parseString(response.body())
                .getAsJsonObject();
        return result.get("content").getAsString();
    }
}
