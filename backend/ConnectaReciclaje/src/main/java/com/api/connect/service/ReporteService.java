package com.api.connect.service;

import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.api.connect.dto.ReporteRequest;
import com.api.connect.entity.User;
import com.api.connect.repository.UserRepository;

import lombok.RequiredArgsConstructor;


@Service
@RequiredArgsConstructor
public class ReporteService {

    private final UserRepository userRepository;
    private final RestTemplate restTemplate;

    public String enviarReporte(String email, ReporteRequest request) {
        //  Buscar el usuario autenticado por su email
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado: " + email));

        //  Puerto fijo (sin importar el rol)
        String url = "http://localhost:8000/transfer";

        //  Cuerpo de la petición que se envía a FastAPI
        Map<String, Object> body = new HashMap<>();
        body.put("user_id", user.getId_usuario());
        body.put("query", request.getQuery());
        body.put("rol", user.getRol());

        try {
            //  Enviar POST al servicio FastAPI
            return restTemplate.postForObject(url, body, String.class);
        } catch (Exception e) {
            return " Error al comunicarse con FastAPI (" + url + "): " + e.getMessage();
        }
    }
}
