package com.api.connect.config;

import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.api.connect.filter.JwtValidationFilter;
@Configuration
public class FilterConfig {

	   @Bean
	    public FilterRegistrationBean<JwtValidationFilter> jwtFilter(JwtValidationFilter jwtValidationFilter) {
	        FilterRegistrationBean<JwtValidationFilter> registration = new FilterRegistrationBean<>();
	        registration.setFilter(jwtValidationFilter); 
	        registration.addUrlPatterns("/api/*");
	        return registration;
	    }
}
