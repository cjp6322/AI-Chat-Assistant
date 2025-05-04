package com.example.minecraftgpt;

import net.fabricmc.api.ClientModInitializer;

public class MinecraftGPTClientMod implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        ClientChatEventHandler.register();
        System.out.println("MinecraftGPT Client (1.21.5) initialized!");
    }
}