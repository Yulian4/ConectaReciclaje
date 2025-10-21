package com.api.connect.service;

import io.jsonwebtoken.*;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

@Service
public class JwtService {

	@Value("${security.jwt.secret-key}")
	private String SECRET_KEY;

	@Value("${security.jwt.expiration}")
	private long EXPIRATION_TIME; // milisegundos

	public String generateToken(String email) {
		Map<String, Object> claims = new HashMap<>();
		return Jwts.builder().setClaims(claims).setSubject(email).setIssuedAt(new Date())
				.setExpiration(new Date(System.currentTimeMillis() + EXPIRATION_TIME)).signWith(getKey()).compact();
	}

	public String extractEmail(String token) {
		return parseToken(token).getBody().getSubject();
	}

	public boolean validateToken(String token) {
		try {
			parseToken(token);
			return true;
		} catch (JwtException e) {
			return false;
		}
	}

	public String refreshToken(String oldToken) {
		if (!validateToken(oldToken)) {
			throw new RuntimeException("Token inválido o expirado");
		}

		String email = extractEmail(oldToken);
		return generateToken(email);
	}

	private Jws<Claims> parseToken(String token) {
		return Jwts.parserBuilder().setSigningKey(getKey()).build().parseClaimsJws(token);
	}

	private SecretKey getKey() {
		return Keys.hmacShaKeyFor(SECRET_KEY.getBytes());
	}
}
