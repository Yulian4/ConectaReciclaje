package com.api.connect.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.api.connect.entity.Town;


public interface TownRepository extends JpaRepository<Town, Integer> { }
