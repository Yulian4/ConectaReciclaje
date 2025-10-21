package com.api.connect.dto;

import lombok.Data;

@Data
public class RegisterRequest {
    private String nombreCompleto;
    private String tipoDoc;
    private String numeroDoc;
    private String telefono;
    private String email;
    private String password;
    private String rol;
    private Integer idDireccion;
}

