# Java Development Best Practices and Anti-Patterns

This document provides additional best practices, common anti-patterns, and practical guidance for production-ready Java applications.

## 1. Common Anti-Patterns to Avoid

### 1.1 Magic Numbers and Strings

**Anti-Pattern:**
```java
// BAD - Hard-coded values
if (status == 1) { ... }
if (userType.equals("ADMIN")) { ... }
connection.setConnectTimeout(30000);
```

**Best Practice:**
```java
// GOOD - Named constants
if (status == OrderStatus.PAID.getCode()) { ... }
if (userType.equals(UserType.ADMIN.name())) { ... }
connection.setConnectTimeout(Constants.DEFAULT_TIMEOUT_MS);
```

### 1.2 Deep Nesting

**Anti-Pattern:**
```java
// BAD - Too many nested levels
public void processOrder(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            if (order.getItems().size() > 0) {
                for (OrderItem item : order.getItems()) {
                    if (item.getProduct() != null) {
                        // ... many more levels
                    }
                }
            }
        }
    }
}
```

**Best Practice:**
```java
// GOOD - Early returns and guard clauses
public void processOrder(Order order) {
    if (order == null || isEmpty(order.getItems())) {
        return;
    }
    
    for (OrderItem item : order.getItems()) {
        processOrderItem(item);
    }
}
```

### 1.3 Swallowing Exceptions

**Anti-Pattern:**
```java
// BAD - Swallowing exceptions
try {
    saveToDatabase();
} catch (Exception e) {
    // Do nothing
}
```

**Best Practice:**
```java
// GOOD - Proper exception handling
try {
    saveToDatabase();
} catch (DatabaseException e) {
    log.error("Failed to save to database: {}", e.getMessage(), e);
    throw new BusinessException("Failed to save data", e);
}
```

### 1.4 Overly General Exceptions

**Anti-Pattern:**
```java
// BAD - Catching too general exceptions
catch (Exception e) { ... }
catch (RuntimeException e) { ... }
```

**Best Practice:**
```java
// GOOD - Catching specific exceptions
catch (SQLException e) {
    log.error("Database error occurred", e);
    throw new BusinessException("Database operation failed", e);
}
catch (IOException e) {
    log.error("IO error occurred", e);
    throw new BusinessException("File operation failed", e);
}
```

### 1.5 String Concatenation in Loops

**Anti-Pattern:**
```java
// BAD - Inefficient string concatenation
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i + ",";
}
```

**Best Practice:**
```java
// GOOD - Using StringBuilder
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i).append(",");
}
String result = sb.toString();
```

### 1.6 Returning Null Instead of Optional

**Anti-Pattern:**
```java
// BAD - Returning null
public User getUser(Long id) {
    return userRepository.findById(id).orElse(null);
}

// Usage
User user = getUser(id);
if (user != null) {
    user.getName();
}
```

**Best Practice:**
```java
// GOOD - Returning Optional
public Optional<User> getUser(Long id) {
    return userRepository.findById(id);
}

// Usage
getUser(id).ifPresent(user -> user.getName());
User user = getUser(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));
```

### 1.7 Unnecessary Synchronization

**Anti-Pattern:**
```java
// BAD - Synchronizing the entire method unnecessarily
public synchronized void processOrder(Order order) {
    // Lots of non-critical code
    String formatted = order.toString();
    List<Item> items = order.getItems();
    
    // Only this part needs synchronization
    counter.increment();
}
```

**Best Practice:**
```java
// GOOD - Synchronizing only the critical section
public void processOrder(Order order) {
    // Non-critical code
    String formatted = order.toString();
    List<Item> items = order.getItems();
    
    // Synchronize only critical section
    synchronized (counterLock) {
        counter.increment();
    }
}
```

### 1.8 Using ArrayList as Queue

**Anti-Pattern:**
```java
// BAD - Using ArrayList as a queue (ineefficient)
List<String> queue = new ArrayList<>();
queue.remove(0); // O(n) operation - shifts all elements
```

**Best Practice:**
```java
// GOOD - Using proper Queue implementation
Queue<String> queue = new LinkedList<>();
queue.poll(); // O(1) operation
```

## 2. Performance Best Practices

### 2.1 Lazy Loading

**Use lazy initialization for expensive objects:**
```java
public class ExpensiveService {
    private ExpensiveObject expensiveObject;
    
    public ExpensiveObject getExpensiveObject() {
        if (expensiveObject == null) {
            expensiveObject = new ExpensiveObject(); // Created only when needed
        }
        return expensiveObject;
    }
}
```

### 2.2 Object Pooling

**Reuse expensive objects instead of creating new ones:**
```java
public class ConnectionPool {
    private final Queue<Connection> availableConnections = new LinkedList<>();
    
    public Connection getConnection() {
        Connection connection = availableConnections.poll();
        if (connection == null) {
            connection = createNewConnection();
        }
        return connection;
    }
    
    public void releaseConnection(Connection connection) {
        availableConnections.offer(connection);
    }
}
```

### 2.3 Streaming Large Collections

**Use streams for large collections instead of loading everything into memory:**
```java
// GOOD - Process large data without loading all into memory
try (Stream<User> userStream = userRepository.streamAll()) {
    userStream
        .filter(user -> user.isActive())
        .map(User::getEmail)
        .forEach(this::sendEmail);
}
```

### 2.4 Batch Processing

**Process items in batches for database operations:**
```java
public void processUsers(List<User> users) {
    final int batchSize = 1000;
    for (int i = 0; i < users.size(); i += batchSize) {
        List<User> batch = users.subList(i, Math.min(i + batchSize, users.size()));
        userRepository.saveAll(batch);
    }
}
```

## 3. Thread Safety Patterns

### 3.1 Immutable Objects

**Prefer immutability for thread safety:**
```java
// GOOD - Immutable class is thread-safe by design
@Immutable
public final class User {
    private final Long id;
    private final String name;
    private final String email;
    
    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Only getters, no setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
}
```

### 3.2 ThreadLocal for Per-Thread State

**Use ThreadLocal for thread-local state:**
```java
public class UserContext {
    private static final ThreadLocal<Long> userIdHolder = new ThreadLocal<>();
    
    public static void setUserId(Long userId) {
        userIdHolder.set(userId);
    }
    
    public static Long getUserId() {
        return userIdHolder.get();
    }
    
    public static void clear() {
        userIdHolder.remove();
    }
}
```

### 3.3 Copy-on-Write for Read-Heavy Collections

**Use CopyOnWriteArrayList for read-heavy scenarios:**
```java
// GOOD - CopyOnWrite for thread-safe read-heavy lists
private final List<Listener> listeners = new CopyOnWriteArrayList<>();

public void addListener(Listener listener) {
    listeners.add(listener);
}

public void notifyListeners(Event event) {
    for (Listener listener : listeners) {
        listener.onEvent(event); // Safe iteration without locks
    }
}
```

## 4. Database Best Practices

### 4.1 Connection Pooling

**Always use connection pooling:**
```java
// HikariCP configuration
@Bean
public DataSource dataSource() {
    HikariConfig config = new HikariConfig();
    config.setJdbcUrl(jdbcUrl);
    config.setUsername(username);
    config.setPassword(password);
    config.setMaximumPoolSize(20);  // Based on your workload
    config.setMinimumIdle(5);
    config.setConnectionTimeout(30000);
    config.setIdleTimeout(600000);
    config.setMaxLifetime(1800000);
    config.setLeakDetectionThreshold(60000);  // Detect connection leaks
    return new HikariDataSource(config);
}
```

### 4.2 Transaction Boundaries

**Keep transactions short and focused:**
```java
// GOOD - Small, focused transaction
@Transactional
public void updateUserStatus(Long userId, String status) {
    User user = userRepository.findById(userId)
        .orElseThrow(() -> new ResourceNotFoundException("User not found"));
    user.setStatus(status);
    userRepository.save(user);
}

// BAD - Long transaction that includes non-DB operations
@Transactional
public void processUser(Long userId) {
    User user = userRepository.findById(userId).get();
    user.setStatus("ACTIVE");
    userRepository.save(user);
    
    // Don't do this in a transaction!
    sendEmail(user.getEmail());  // External API call in transaction
    generateReport(user);        // Heavy computation in transaction
}
```

### 4.3 Batching SQL Operations

**Use batch updates for multiple operations:**
```java
// GOOD - Batch insert
public void batchInsertUsers(List<User> users) {
    String sql = "INSERT INTO users (username, email) VALUES (?, ?)";
    
    try (Connection conn = dataSource.getConnection();
         PreparedStatement stmt = conn.prepareStatement(sql)) {
        
        for (User user : users) {
            stmt.setString(1, user.getUsername());
            stmt.setString(2, user.getEmail());
            stmt.addBatch();
        }
        
        stmt.executeBatch();
    } catch (SQLException e) {
        log.error("Batch insert failed", e);
        throw new BusinessException("Batch insert failed", e);
    }
}
```

## 5. API Design Best Practices

### 5.1 Consistent Response Structure

**Use consistent API response structure:**
```java
public class ApiResponse<T> {
    private boolean success;
    private String message;
    private T data;
    private String errorCode;
    private long timestamp;
    
    // Factory methods
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, "Success", data, null, System.currentTimeMillis());
    }
    
    public static <T> ApiResponse<T> error(String errorCode, String message) {
        return new ApiResponse<>(false, message, null, errorCode, System.currentTimeMillis());
    }
}

// Usage
@GetMapping("/users/{id}")
public ApiResponse<UserDTO> getUser(@PathVariable Long id) {
    UserDTO user = userService.getUserById(id);
    return ApiResponse.success(user);
}
```

### 5.2 API Versioning

**Implement proper API versioning:**
```java
// URL versioning
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 { ... }

@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 { ... }

// Header versioning
@GetMapping("/api/users")
public ResponseEntity<?> getUser(@RequestHeader("API-Version") String version) {
    if ("v1".equals(version)) {
        return ResponseEntity.ok(userServiceV1.getUser());
    } else if ("v2".equals(version)) {
        return ResponseEntity.ok(userServiceV2.getUser());
    }
    return ResponseEntity.status(HttpStatus.NOT_ACCEPTABLE).build();
}
```

### 5.3 Pagination for Large Data Sets

**Always implement pagination for list endpoints:**
```java
@GetMapping("/users")
public ResponseEntity<Page<UserDTO>> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(defaultValue = "createdAt") String sortBy,
        @RequestParam(defaultValue = "desc") String direction) {
    
    // Validate and limit page size
    size = Math.min(size, 100);
    
    Sort sort = direction.equalsIgnoreCase("desc") 
            ? Sort.by(sortBy).descending()
            : Sort.by(sortBy).ascending();
    
    Pageable pageable = PageRequest.of(page, size, sort);
    Page<UserDTO> users = userService.getUsers(pageable);
    
    return ResponseEntity.ok(users);
}
```

## 6. Security Best Practices

### 6.1 Input Validation

**Validate all inputs at multiple layers:**
```java
// Controller layer validation
@PostMapping("/users")
public ResponseEntity<?> createUser(@Valid @RequestBody CreateUserRequest request) {
    // If validation fails, Spring automatically returns 400
    return ResponseEntity.ok(userService.createUser(request));
}

// Service layer validation
public User createUser(CreateUserRequest request) {
    // Additional business logic validation
    if (userRepository.existsByEmail(request.getEmail())) {
        throw new BusinessException("Email already exists", ErrorCode.EMAIL_EXISTS);
    }
    // ...
}
```

### 6.2 Secure Password Storage

**Use strong password hashing:**
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);  // Strength 12
}

// Usage
String hashedPassword = passwordEncoder.encode(rawPassword);
boolean matches = passwordEncoder.matches(rawPassword, hashedPassword);
```

### 6.3 Prevent SQL Injection

**Always use parameterized queries:**
```java
// GOOD - Parameterized query
String sql = "SELECT * FROM users WHERE email = ?";
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.setString(1, email);
ResultSet rs = stmt.executeQuery();

// BAD - String concatenation (vulnerable to SQL injection)
String sql = "SELECT * FROM users WHERE email = '" + email + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);
```

### 6.4 Secure Logging

**Never log sensitive information:**
```java
// BAD - Logging sensitive data
log.info("User login: username={}, password={}", username, password);
log.info("Payment processed: cardNumber={}, cvv={}", cardNumber, cvv);

// GOOD - Logging minimal information
log.info("User login attempt: username={}", username);
log.info("Payment processed: userId={}, amount={}", userId, amount);
```

## 7. Error Handling Best Practices

### 7.1 Exception Hierarchy

**Design a clear exception hierarchy:**
```
RuntimeException
└── BusinessException
    ├── ValidationException
    ├── ResourceNotFoundException
    ├── DuplicateResourceException
    └── AuthenticationException
```

### 7.2 Global Exception Handling

**Use global exception handler for consistent error responses:**
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusinessException(BusinessException ex) {
        ErrorResponse error = new ErrorResponse(
            ex.getErrorCode().getCode(),
            ex.getMessage(),
            System.currentTimeMillis()
        );
        return ResponseEntity.badRequest().body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {
        log.error("Unexpected error", ex);
        ErrorResponse error = new ErrorResponse(
            500,
            "Internal server error",
            System.currentTimeMillis()
        );
        return ResponseEntity.status(500).body(error);
    }
}
```

## 8. Testing Best Practices

### 8.1 Test Naming Conventions

**Use descriptive test names:**
```java
// GOOD - Descriptive names
@Test
public void shouldReturnUserWhenUserExists() { ... }

@Test
public void shouldThrowExceptionWhenUserNotFound() { ... }

@Test
public void shouldUpdateUserStatusWhenStatusIsValid() { ... }

// BAD - Generic names
@Test
public void testUser() { ... }

@Test
public void test1() { ... }
```

### 8.2 AAA Pattern

**Structure tests using Arrange-Act-Assert pattern:**
```java
@Test
public void shouldUpdateUserStatus() {
    // Arrange
    Long userId = 1L;
    User existingUser = User.builder().id(userId).status("ACTIVE").build();
    when(userRepository.findById(userId)).thenReturn(Optional.of(existingUser));
    
    // Act
    userService.updateUserStatus(userId, "INACTIVE");
    
    // Assert
    verify(userRepository).save(argThat(user -> 
        user.getStatus().equals("INACTIVE")
    ));
}
```

### 8.3 Test Isolation

**Ensure tests are independent and isolated:**
```java
// GOOD - Each test cleans up after itself
@Test
public void testCreateUser() {
    User user = userRepository.save(testUser);
    assertThat(userRepository.findById(user.getId())).isPresent();
    
    // Cleanup
    userRepository.deleteById(user.getId());
}

// BETTER - Use @BeforeEach and @AfterEach
@BeforeEach
void setUp() {
    testUser = User.builder().username("test").email("test@example.com").build();
}

@AfterEach
void tearDown() {
    userRepository.deleteAll();
}
```

## 9. Code Organization

### 9.1 Package Structure

**Follow clear package structure:**
```
com.alibaba.project
├── config          # Configuration classes
├── controller      # REST controllers
├── dto            # Data transfer objects
│   ├── request    # Request DTOs
│   └── response   # Response DTOs
├── entity         # JPA entities
├── exception      # Custom exceptions
├── mapper         # Entity-DTO mappers
├── repository     # Repository interfaces
├── service        # Service interfaces
│   └── impl       # Service implementations
├── util           # Utility classes
└── Application.java
```

### 9.2 Separation of Concerns

**Maintain clear separation between layers:**
- **Controller**: Handle HTTP requests/responses, validation, routing
- **Service**: Business logic, transactions, orchestration
- **Repository**: Data access, database operations
- **Entity**: Data model, database mapping
- **DTO**: Data transfer between layers

## 10. Monitoring and Observability

### 10.1 Structured Logging

**Use structured logging for better log parsing:**
```java
// GOOD - Structured logging
log.info("User login: {}", JsonLog.of()
    .put("userId", userId)
    .put("ip", request.getRemoteAddr())
    .put("timestamp", Instant.now())
    .put("success", true)
);

// Output: {"userId":"123","ip":"192.168.1.1","timestamp":"2024-01-01T12:00:00Z","success":"true"}
```

### 10.2 Metrics

**Track key metrics:**
```java
// Using Micrometer
@Autowired
private MeterRegistry meterRegistry;

public void processOrder(Order order) {
    Timer.Sample sample = Timer.start(meterRegistry);
    try {
        // Process order
        meterRegistry.counter("orders.processed", "status", "success").increment();
    } catch (Exception e) {
        meterRegistry.counter("orders.processed", "status", "failed").increment();
        throw e;
    } finally {
        sample.stop(Timer.builder("orders.processing.time").register(meterRegistry));
    }
}
```

### 10.3 Health Checks

**Implement health check endpoints:**
```java
@RestController
@RequestMapping("/health")
public class HealthController {
    
    @Autowired
    private DataSource dataSource;
    
    @GetMapping
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", Instant.now().toString());
        
        // Check database connectivity
        try (Connection conn = dataSource.getConnection()) {
            health.put("database", "UP");
        } catch (SQLException e) {
            health.put("database", "DOWN");
            health.put("status", "DOWN");
        }
        
        return ResponseEntity.ok(health);
    }
}
```

## 11. Documentation

### 11.1 JavaDoc Standards

**Write comprehensive JavaDoc:**
```java
/**
 * Service for managing user operations.
 * 
 * <p>This service provides methods for creating, retrieving, updating, 
 * and deleting users in the system. All operations are transactional and 
 * follow the business rules defined in the system.</p>
 *
 * <p>Example usage:
 * <pre>{@code
 * UserDTO user = userService.createUser(request);
 * List<UserDTO> users = userService.getAllUsers();
 * }</pre></p>
 *
 * @author John Doe
 * @version 1.0
 * @since 2024-01-01
 */
public interface UserService {
    
    /**
     * Creates a new user in the system.
     *
     * <p>This method validates the user input, checks for duplicate email,
     * and saves the user to the database. The password is automatically
     * hashed before storage.</p>
     *
     * @param request the user creation request, must not be null
     * @return the created user with assigned ID
     * @throws BusinessException if email already exists
     * @throws IllegalArgumentException if request is null or invalid
     * @see CreateUserRequest
     */
    UserDTO createUser(CreateUserRequest request);
}
```

### 11.2 API Documentation

**Use OpenAPI/Swagger for API documentation:**
```java
@Operation(summary = "Create a new user", description = "Creates a user with the provided information")
@ApiResponses(value = {
    @ApiResponse(responseCode = "201", description = "User created successfully"),
    @ApiResponse(responseCode = "400", description = "Invalid input data"),
    @ApiResponse(responseCode = "409", description = "Email already exists")
})
@PostMapping
public ResponseEntity<UserDTO> createUser(
        @Parameter(description = "User creation request", required = true)
        @Valid @RequestBody CreateUserRequest request) {
    // ...
}
```

These best practices will help you maintain high-quality, production-ready Java applications that are secure, performant, and maintainable.
