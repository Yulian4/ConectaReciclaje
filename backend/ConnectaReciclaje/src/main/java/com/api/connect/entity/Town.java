package com.api.connect.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "barrio")
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Town {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id_barrio;

    @Column(nullable = false)
    private String nombre;
}
