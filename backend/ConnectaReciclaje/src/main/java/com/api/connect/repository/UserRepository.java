package com.api.connect.repository;


import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.api.connect.entity.User;

public interface UserRepository extends JpaRepository<User, Integer> {
    Optional<User> findByEmail(String email);
}

