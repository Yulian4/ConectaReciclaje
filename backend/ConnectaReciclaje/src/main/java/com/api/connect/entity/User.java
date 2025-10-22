package com.api.connect.entity;

import java.time.LocalDateTime;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "usuarios")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_usuario;

    private String nombre_completo;
    private String tipo_doc;
    private String numero_doc;
    private String telefono;
    private String email;
    private String rol;
    private String password;

    @ManyToOne
    @JoinColumn(name = "id_direccion")
    private Adress direccion;

    @Column(name = "fecha_registro", insertable = false, updatable = false)
    private LocalDateTime fecha_registro;
}
