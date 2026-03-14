# Java Code Templates and Common Patterns

This document provides reusable code templates and patterns following Alibaba Taishan standards.

## 1. Controller Templates

### 1.1 REST Controller

```java
package com.alibaba.project.controller;

import com.alibaba.project.dto.UserDTO;
import com.alibaba.project.request.CreateUserRequest;
import com.alibaba.project.request.UpdateUserRequest;
import com.alibaba.project.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import javax.validation.constraints.Positive;
import java.util.List;

/**
 * User controller for user management operations.
 */
@Slf4j
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
@Validated
public class UserController {

    private final UserService userService;

    /**
     * Get user by ID.
     *
     * @param id the user ID
     * @return the user details
     */
    @GetMapping("/{id}")
    public ResponseEntity<UserDTO> getUser(
            @Positive(message = "ID must be positive") 
            @PathVariable Long id) {
        log.info("Getting user by ID: {}", id);
        UserDTO user = userService.getUserById(id);
        return ResponseEntity.ok(user);
    }

    /**
     * Get all users with pagination.
     *
     * @param page page number (0-based)
     * @param size page size
     * @return paginated list of users
     */
    @GetMapping
    public ResponseEntity<Page<UserDTO>> getUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size) {
        
        // Enforce maximum page size
        if (size > 100) {
            size = 100;
        }
        
        log.info("Getting users: page={}, size={}", page, size);
        Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
        Page<UserDTO> users = userService.getUsers(pageable);
        return ResponseEntity.ok(users);
    }

    /**
     * Create a new user.
     *
     * @param request the user creation request
     * @return the created user
     */
    @PostMapping
    public ResponseEntity<UserDTO> createUser(
            @Valid @RequestBody CreateUserRequest request) {
        log.info("Creating user: username={}", request.getUsername());
        UserDTO user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }

    /**
     * Update an existing user.
     *
     * @param id      the user ID
     * @param request the update request
     * @return the updated user
     */
    @PutMapping("/{id}")
    public ResponseEntity<UserDTO> updateUser(
            @Positive(message = "ID must be positive")
            @PathVariable Long id,
            @Valid @RequestBody UpdateUserRequest request) {
        log.info("Updating user: id={}", id);
        UserDTO user = userService.updateUser(id, request);
        return ResponseEntity.ok(user);
    }

    /**
     * Delete a user.
     *
     * @param id the user ID
     * @return no content response
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(
            @Positive(message = "ID must be positive")
            @PathVariable Long id) {
        log.info("Deleting user: id={}", id);
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }
}
```

### 1.2 Controller with Global Exception Handling

```java
package com.alibaba.project.exception;

import com.alibaba.project.dto.ErrorResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import javax.servlet.http.HttpServletRequest;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * Global exception handler for REST controllers.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Handle business exceptions.
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(
            BusinessException ex,
            HttpServletRequest request) {
        log.error("Business exception: {}", ex.getMessage(), ex);
        
        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error("Business Error")
                .message(ex.getMessage())
                .code(ex.getErrorCode().getCode())
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
     * Handle resource not found exceptions.
     */
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleResourceNotFoundException(
            ResourceNotFoundException ex,
            HttpServletRequest request) {
        log.error("Resource not found: {}", ex.getMessage());
        
        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.NOT_FOUND.value())
                .error("Not Found")
                .message(ex.getMessage())
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }

    /**
     * Handle validation exceptions.
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidationException(
            MethodArgumentNotValidException ex,
            HttpServletRequest request) {
        log.error("Validation exception: {}", ex.getMessage());
        
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getAllErrors().forEach(error -> {
            String fieldName = ((FieldError) error).getField();
            String errorMessage = error.getDefaultMessage();
            errors.put(fieldName, errorMessage);
        });
        
        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.BAD_REQUEST.value())
                .error("Validation Failed")
                .message("Invalid request parameters")
                .validationErrors(errors)
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(error);
    }

    /**
     * Handle all other exceptions.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(
            Exception ex,
            HttpServletRequest request) {
        log.error("Unexpected exception: {}", ex.getMessage(), ex);
        
        ErrorResponse error = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.INTERNAL_SERVER_ERROR.value())
                .error("Internal Server Error")
                .message("An unexpected error occurred")
                .path(request.getRequestURI())
                .build();
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}
```

## 2. Service Layer Templates

### 2.1 Service Interface

```java
package com.alibaba.project.service;

import com.alibaba.project.dto.UserDTO;
import com.alibaba.project.request.CreateUserRequest;
import com.alibaba.project.request.UpdateUserRequest;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

/**
 * User service interface for user business logic.
 */
public interface UserService {

    /**
     * Get user by ID.
     *
     * @param id the user ID
     * @return the user details
     * @throws ResourceNotFoundException if user not found
     */
    UserDTO getUserById(Long id);

    /**
     * Get all users with pagination.
     *
     * @param pageable pagination information
     * @return paginated list of users
     */
    Page<UserDTO> getUsers(Pageable pageable);

    /**
     * Create a new user.
     *
     * @param request the user creation request
     * @return the created user
     * @throws BusinessException if user creation fails
     */
    UserDTO createUser(CreateUserRequest request);

    /**
     * Update an existing user.
     *
     * @param id      the user ID
     * @param request the update request
     * @return the updated user
     * @throws ResourceNotFoundException if user not found
     * @throws BusinessException if update fails
     */
    UserDTO updateUser(Long id, UpdateUserRequest request);

    /**
     * Delete a user.
     *
     * @param id the user ID
     * @throws ResourceNotFoundException if user not found
     */
    void deleteUser(Long id);

    /**
     * Check if user exists by email.
     *
     * @param email the email address
     * @return true if user exists, false otherwise
     */
    boolean existsByEmail(String email);
}
```

### 2.2 Service Implementation

```java
package com.alibaba.project.service.impl;

import com.alibaba.project.dto.UserDTO;
import com.alibaba.project.entity.User;
import com.alibaba.project.exception.BusinessException;
import com.alibaba.project.exception.ErrorCode;
import com.alibaba.project.exception.ResourceNotFoundException;
import com.alibaba.project.mapper.UserMapper;
import com.alibaba.project.repository.UserRepository;
import com.alibaba.project.request.CreateUserRequest;
import com.alibaba.project.request.UpdateUserRequest;
import com.alibaba.project.service.UserService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * User service implementation.
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;
    private final PasswordEncoder passwordEncoder;

    @Override
    @Transactional(readOnly = true)
    public UserDTO getUserById(Long id) {
        log.debug("Getting user by ID: {}", id);
        User user = userRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("User not found with ID: {}", id);
                    return new ResourceNotFoundException("User not found with ID: " + id);
                });
        return userMapper.toDTO(user);
    }

    @Override
    @Transactional(readOnly = true)
    public Page<UserDTO> getUsers(Pageable pageable) {
        log.debug("Getting users: pageable={}", pageable);
        return userRepository.findAll(pageable)
                .map(userMapper::toDTO);
    }

    @Override
    @Transactional
    public UserDTO createUser(CreateUserRequest request) {
        log.info("Creating user: username={}", request.getUsername());
        
        // Check if email already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            log.warn("Email already exists: {}", request.getEmail());
            throw new BusinessException(
                    "Email already exists: " + request.getEmail(),
                    ErrorCode.EMAIL_ALREADY_EXISTS);
        }
        
        // Create user entity
        User user = userMapper.toEntity(request);
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        
        // Save user
        User savedUser = userRepository.save(user);
        log.info("User created successfully: id={}", savedUser.getId());
        
        return userMapper.toDTO(savedUser);
    }

    @Override
    @Transactional
    public UserDTO updateUser(Long id, UpdateUserRequest request) {
        log.info("Updating user: id={}", id);
        
        User user = userRepository.findById(id)
                .orElseThrow(() -> {
                    log.error("User not found with ID: {}", id);
                    return new ResourceNotFoundException("User not found with ID: " + id);
                });
        
        // Check if email is being changed and if new email exists
        if (!user.getEmail().equals(request.getEmail()) 
                && userRepository.existsByEmail(request.getEmail())) {
            log.warn("Email already exists: {}", request.getEmail());
            throw new BusinessException(
                    "Email already exists: " + request.getEmail(),
                    ErrorCode.EMAIL_ALREADY_EXISTS);
        }
        
        // Update user fields
        userMapper.updateEntity(user, request);
        
        User savedUser = userRepository.save(user);
        log.info("User updated successfully: id={}", savedUser.getId());
        
        return userMapper.toDTO(savedUser);
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        log.info("Deleting user: id={}", id);
        
        if (!userRepository.existsById(id)) {
            log.error("User not found with ID: {}", id);
            throw new ResourceNotFoundException("User not found with ID: " + id);
        }
        
        userRepository.deleteById(id);
        log.info("User deleted successfully: id={}", id);
    }

    @Override
    @Transactional(readOnly = true)
    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }
}
```

## 3. Repository Templates

### 3.1 JPA Repository

```java
package com.alibaba.project.repository;

import com.alibaba.project.entity.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * User repository for database operations.
 */
@Repository
public interface UserRepository extends JpaRepository<User, Long>, JpaSpecificationExecutor<User> {

    /**
     * Find user by email.
     *
     * @param email the email address
     * @return optional user
     */
    Optional<User> findByEmail(String email);

    /**
     * Check if user exists by email.
     *
     * @param email the email address
     * @return true if exists, false otherwise
     */
    boolean existsByEmail(String email);

    /**
     * Find users by status with pagination.
     *
     * @param status   the user status
     * @param pageable pagination information
     * @return paginated list of users
     */
    Page<User> findByStatus(String status, Pageable pageable);

    /**
     * Find user with roles fetched eagerly to avoid N+1 query problem.
     *
     * @param id the user ID
     * @return optional user with roles
     */
    @Query("SELECT u FROM User u LEFT JOIN FETCH u.roles WHERE u.id = :id")
    Optional<User> findByIdWithRoles(@Param("id") Long id);

    /**
     * Count users by status.
     *
     * @param status the user status
     * @return count of users
     */
    long countByStatus(String status);
}
```

## 4. Entity Templates

### 4.1 JPA Entity

```java
package com.alibaba.project.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * User entity representing a user in the system.
 */
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_user_email", columnList = "email"),
    @Index(name = "idx_user_status", columnList = "status")
})
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
    @Column(name = "username", nullable = false, unique = true, length = 20)
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @NotBlank(message = "Password is required")
    @Column(name = "password", nullable = false)
    private String password;

    @Column(name = "status", nullable = false, length = 20)
    @Builder.Default
    private String status = "ACTIVE";

    @Column(name = "enabled", nullable = false)
    @Builder.Default
    private Boolean enabled = true;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    @Builder.Default
    private Set<Role> roles = new HashSet<>();

    /**
     * Check if user has the specified role.
     *
     * @param roleName the role name
     * @return true if user has the role, false otherwise
     */
    public boolean hasRole(String roleName) {
        return roles.stream()
                .anyMatch(role -> role.getName().equals(roleName));
    }
}
```

## 5. DTO Templates

### 5.1 Request DTO

```java
package com.alibaba.project.request;

import lombok.Data;

import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import javax.validation.constraints.Size;

/**
 * Request DTO for creating a user.
 */
@Data
public class CreateUserRequest {

    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
    private String username;

    @NotBlank(message = "Email is required")
    @Email(message = "Invalid email format")
    private String email;

    @NotBlank(message = "Password is required")
    @Size(min = 8, max = 100, message = "Password must be between 8 and 100 characters")
    @Pattern(regexp = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\\S+$).{8,}$",
            message = "Password must contain uppercase, lowercase, digit, and special character")
    private String password;

    @Pattern(regexp = "^\\+?[0-9]{10,15}$", message = "Invalid phone number format")
    private String phone;

    private String firstName;

    private String lastName;
}

/**
 * Request DTO for updating a user.
 */
@Data
public class UpdateUserRequest {

    @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
    private String username;

    @Email(message = "Invalid email format")
    private String email;

    @Pattern(regexp = "^\\+?[0-9]{10,15}$", message = "Invalid phone number format")
    private String phone;

    private String firstName;

    private String lastName;

    private String status;

    private Boolean enabled;
}
```

### 5.2 Response DTO

```java
package com.alibaba.project.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Set;

/**
 * Response DTO for user information.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDTO {

    private Long id;
    private String username;
    private String email;
    private String phone;
    private String firstName;
    private String lastName;
    private String status;
    private Boolean enabled;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private Set<RoleDTO> roles;
}
```

### 5.3 Error Response DTO

```java
package com.alibaba.project.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Error response DTO for API errors.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponse {

    private LocalDateTime timestamp;
    private int status;
    private String error;
    private String message;
    private String code;
    private String path;
    private Map<String, String> validationErrors;
}
```

## 6. Exception Templates

### 6.1 Custom Exception

```java
package com.alibaba.project.exception;

import lombok.Getter;

/**
 * Base business exception for application-specific errors.
 */
@Getter
public class BusinessException extends RuntimeException {

    private final ErrorCode errorCode;

    public BusinessException(String message, ErrorCode errorCode) {
        super(message);
        this.errorCode = errorCode;
    }

    public BusinessException(String message, ErrorCode errorCode, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
}

/**
 * Resource not found exception.
 */
@Getter
public class ResourceNotFoundException extends RuntimeException {

    private final String resourceType;
    private final Long resourceId;

    public ResourceNotFoundException(String message) {
        super(message);
        this.resourceType = null;
        this.resourceId = null;
    }

    public ResourceNotFoundException(String resourceType, Long resourceId) {
        super(String.format("%s not found with ID: %d", resourceType, resourceId));
        this.resourceType = resourceType;
        this.resourceId = resourceId;
    }
}

/**
 * Error code enum.
 */
@Getter
public enum ErrorCode {

    // Business errors
    EMAIL_ALREADY_EXISTS(1001, "Email already exists"),
    INVALID_CREDENTIALS(1002, "Invalid credentials"),
    ACCOUNT_DISABLED(1003, "Account is disabled"),
    
    // Validation errors
    INVALID_INPUT(2001, "Invalid input parameter"),
    
    // System errors
    INTERNAL_ERROR(5001, "Internal system error"),
    DATABASE_ERROR(5002, "Database operation failed"),
    EXTERNAL_SERVICE_ERROR(5003, "External service error");

    private final int code;
    private final String message;

    ErrorCode(int code, String message) {
        this.code = code;
        this.message = message;
    }
}
```

## 7. Mapper Templates

### 7.1 DTO-Entity Mapper

```java
package com.alibaba.project.mapper;

import com.alibaba.project.dto.UserDTO;
import com.alibaba.project.entity.User;
import com.alibaba.project.request.CreateUserRequest;
import com.alibaba.project.request.UpdateUserRequest;
import org.springframework.stereotype.Component;

/**
 * Mapper for converting between User entities and DTOs.
 */
@Component
public class UserMapper {

    /**
     * Convert User entity to UserDTO.
     *
     * @param user the user entity
     * @return the user DTO
     */
    public UserDTO toDTO(User user) {
        if (user == null) {
            return null;
        }

        return UserDTO.builder()
                .id(user.getId())
                .username(user.getUsername())
                .email(user.getEmail())
                .phone(user.getPhone())
                .firstName(user.getFirstName())
                .lastName(user.getLastName())
                .status(user.getStatus())
                .enabled(user.getEnabled())
                .createdAt(user.getCreatedAt())
                .updatedAt(user.getUpdatedAt())
                .build();
    }

    /**
     * Convert CreateUserRequest to User entity.
     *
     * @param request the create user request
     * @return the user entity
     */
    public User toEntity(CreateUserRequest request) {
        if (request == null) {
            return null;
        }

        return User.builder()
                .username(request.getUsername())
                .email(request.getEmail())
                .phone(request.getPhone())
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .status("ACTIVE")
                .enabled(true)
                .build();
    }

    /**
     * Update User entity from UpdateUserRequest.
     *
     * @param user    the user entity to update
     * @param request the update user request
     */
    public void updateEntity(User user, UpdateUserRequest request) {
        if (request == null || user == null) {
            return;
        }

        if (request.getUsername() != null) {
            user.setUsername(request.getUsername());
        }
        if (request.getEmail() != null) {
            user.setEmail(request.getEmail());
        }
        if (request.getPhone() != null) {
            user.setPhone(request.getPhone());
        }
        if (request.getFirstName() != null) {
            user.setFirstName(request.getFirstName());
        }
        if (request.getLastName() != null) {
            user.setLastName(request.getLastName());
        }
        if (request.getStatus() != null) {
            user.setStatus(request.getStatus());
        }
        if (request.getEnabled() != null) {
            user.setEnabled(request.getEnabled());
        }
    }
}
```

## 8. Configuration Templates

### 8.1 Application Configuration

```java
package com.alibaba.project.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Application configuration beans.
 */
@Configuration
public class AppConfig {

    /**
     * Password encoder bean.
     *
     * @return password encoder
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### 8.2 Database Configuration

```java
package com.alibaba.project.config;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import javax.sql.DataSource;

/**
 * Database configuration.
 */
@Configuration
public class DatabaseConfig {

    @Bean
    @Primary
    @ConfigurationProperties(prefix = "spring.datasource.hikari")
    public DataSource dataSource() {
        HikariConfig config = new HikariConfig();
        config.setPoolName("ProjectHikariPool");
        config.setMaximumPoolSize(20);
        config.setMinimumIdle(5);
        config.setConnectionTimeout(30000);
        config.setIdleTimeout(600000);
        config.setMaxLifetime(1800000);
        config.setConnectionTestQuery("SELECT 1");
        return new HikariDataSource(config);
    }
}
```

### 8.3 Cache Configuration

```java
package com.alibaba.project.config;

import com.github.benmanes.caffeine.cache.Caffeine;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

/**
 * Cache configuration using Caffeine.
 */
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public Caffeine<Object, Object> caffeineConfig() {
        return Caffeine.newBuilder()
                .expireAfterWrite(10, TimeUnit.MINUTES)
                .maximumSize(1000)
                .recordStats();
    }

    @Bean
    public CacheManager cacheManager(Caffeine<Object, Object> caffeine) {
        CaffeineCacheManager caffeineCacheManager = new CaffeineCacheManager();
        caffeineCacheManager.setCaffeine(caffeine);
        return caffeineCacheManager;
    }
}
```

### 8.4 Async Configuration

```java
package com.alibaba.project.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

/**
 * Async task executor configuration.
 */
@Configuration
@EnableAsync
public class AsyncConfig {

    @Bean(name = "taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("Async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}
```

## 9. Utility Templates

### 9.1 Date Utility

```java
package com.alibaba.project.util;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;

/**
 * Date utility class.
 */
public final class DateUtil {

    private static final DateTimeFormatter DEFAULT_FORMATTER = 
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    private DateUtil() {
        throw new UnsupportedOperationException("Utility class");
    }

    /**
     * Format LocalDateTime to default string format.
     *
     * @param dateTime the date time
     * @return formatted string
     */
    public static String format(LocalDateTime dateTime) {
        if (dateTime == null) {
            return null;
        }
        return dateTime.format(DEFAULT_FORMATTER);
    }

    /**
     * Parse string to LocalDateTime.
     *
     * @param dateTimeStr the date time string
     * @return LocalDateTime
     * @throws DateTimeParseException if parsing fails
     */
    public static LocalDateTime parse(String dateTimeStr) {
        if (dateTimeStr == null || dateTimeStr.isEmpty()) {
            return null;
        }
        return LocalDateTime.parse(dateTimeStr, DEFAULT_FORMATTER);
    }

    /**
     * Check if date is in the past.
     *
     * @param dateTime the date time
     * @return true if in the past, false otherwise
     */
    public static boolean isPast(LocalDateTime dateTime) {
        return dateTime != null && dateTime.isBefore(LocalDateTime.now());
    }
}
```

### 9.2 Validation Utility

```java
package com.alibaba.project.util;

import org.springframework.util.StringUtils;

import java.util.Collection;
import java.util.Objects;

/**
 * Validation utility class.
 */
public final class ValidationUtil {

    private ValidationUtil() {
        throw new UnsupportedOperationException("Utility class");
    }

    /**
     * Check if string is null or empty.
     *
     * @param str the string to check
     * @return true if null or empty, false otherwise
     */
    public static boolean isEmpty(String str) {
        return !StringUtils.hasText(str);
    }

    /**
     * Check if collection is null or empty.
     *
     * @param collection the collection to check
     * @return true if null or empty, false otherwise
     */
    public static boolean isEmpty(Collection<?> collection) {
        return collection == null || collection.isEmpty();
    }

    /**
     * Validate that object is not null.
     *
     * @param object   the object to validate
     * @param fieldName the field name for error message
     * @throws IllegalArgumentException if object is null
     */
    public static void requireNonNull(Object object, String fieldName) {
        Objects.requireNonNull(object, fieldName + " must not be null");
    }
}
```

These templates provide a solid foundation for Java development following Alibaba Taishan standards. Adapt them as needed for specific project requirements.
