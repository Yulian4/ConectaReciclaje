package com.api.connect.service;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.api.connect.dto.LoginRequest;
import com.api.connect.dto.LoginResponse;
import com.api.connect.dto.RefreshResponse;
import com.api.connect.dto.RegisterRequest;
import com.api.connect.dto.RegisterResponse;
import com.api.connect.entity.Adress;
import com.api.connect.entity.User;
import com.api.connect.repository.AdressRepository;
import com.api.connect.repository.UserRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {

	private final AdressRepository adressRepository;
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

   public RegisterResponse register(RegisterRequest request) {
        Adress direccion = adressRepository.findById(request.getIdDireccion())
                .orElseThrow(() -> new RuntimeException("Dirección no encontrada"));

        User user = User.builder()
                .nombre_completo(request.getNombreCompleto())
                .tipo_doc(request.getTipoDoc())
                .numero_doc(request.getNumeroDoc())
                .telefono(request.getTelefono())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .rol(request.getRol())
                .direccion(direccion)
                .build();

        userRepository.save(user);
        return new RegisterResponse("Usuario registrado con éxito");
    }
    public LoginResponse login(LoginRequest request) {
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Contraseña incorrecta");
        }

        String token = jwtService.generateToken(user.getEmail());
        return new LoginResponse(token);
    }

    public RefreshResponse refreshToken(String oldToken) {
        String newToken = jwtService.refreshToken(oldToken);
        return new RefreshResponse(newToken);
    }
}
