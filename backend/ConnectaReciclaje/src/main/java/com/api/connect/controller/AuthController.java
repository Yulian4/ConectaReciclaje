package com.api.connect.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.api.connect.dto.LoginRequest;
import com.api.connect.dto.LoginResponse;
import com.api.connect.dto.RefreshResponse;
import com.api.connect.dto.RegisterRequest;
import com.api.connect.dto.RegisterResponse;
import com.api.connect.service.AuthService;

import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @PostMapping("/register")
    public ResponseEntity<RegisterResponse> register(@RequestBody RegisterRequest request) {
        return ResponseEntity.ok(authService.register(request));
    }

    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @PostMapping("/refresh")
    public ResponseEntity<RefreshResponse> refresh(@RequestHeader("Authorization") String authHeader) {
        String oldToken = authHeader.replace("Bearer ", "");
        return ResponseEntity.ok(authService.refreshToken(oldToken));
    }
}
