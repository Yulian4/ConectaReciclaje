package com.api.connect.controller;


import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.api.connect.dto.ReporteRequest;
import com.api.connect.service.ReporteService;

import jakarta.servlet.http.HttpServletRequest;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/reportes")
@RequiredArgsConstructor
public class ReporteController {

    private final ReporteService reporteService;

    @PostMapping
    public ResponseEntity<String> crearReporte(
            @RequestBody ReporteRequest request,
            HttpServletRequest httpRequest
    ) {
        // ✅ Obtener el email que dejó el filtro
        String email = (String) httpRequest.getAttribute("userEmail");

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Usuario no autenticado o token inválido");
        }

        String resultado = reporteService.enviarReporte(email, request);
        return ResponseEntity.ok(resultado);
    }
}

