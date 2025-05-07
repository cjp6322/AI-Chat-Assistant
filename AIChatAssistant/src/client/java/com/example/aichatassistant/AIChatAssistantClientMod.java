package com.example.aichatassistant;

import net.fabricmc.api.ClientModInitializer;

public class AIChatAssistantClientMod implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ClientChatEventHandler.register();
        System.out.println("AIChatAssistant Client (1.21.5) initialized!");
    }
}