package com.example.aichatassistant;

import com.example.aichatassistant.OllamaService;
import net.fabricmc.fabric.api.client.message.v1.ClientSendMessageEvents;
import net.minecraft.client.MinecraftClient;
import net.minecraft.text.Text;

import java.io.IOException;
import java.util.concurrent.CompletableFuture;

public class ClientChatEventHandler {
    public static void register() {
        ClientSendMessageEvents.ALLOW_CHAT.register(message -> {
            if (message.startsWith("?ask ")) {
                String question = message.substring(5).trim();

                // run the HTTP request off the main thread
                CompletableFuture.runAsync(() -> {
                    try {
                        String answer = OllamaService.getInstance().ask(question);
                        // back to client thread to display the response
                        MinecraftClient.getInstance().execute(() ->
                                MinecraftClient.getInstance()
                                        .inGameHud
                                        .getChatHud()
                                        .addMessage(Text.of("§6[AI Chat Assistant]§r " + answer))
                        );
                    } catch (IOException | InterruptedException e) {
                        e.printStackTrace();
                        MinecraftClient.getInstance().execute(() ->
                                MinecraftClient.getInstance()
                                        .inGameHud
                                        .getChatHud()
                                        .addMessage(Text.of("§c[AI Chat Assistant Error]§r " + e.getMessage()))
                        );
                    }
                });

                return false; // block the original “?ask” message from sending
            }
            return true;
        });
    }
}
