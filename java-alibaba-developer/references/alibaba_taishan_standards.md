# Alibaba Taishan Java Development Standards - Detailed Reference

This document provides detailed excerpts from the Alibaba Taishan Java Development Manual (泰山版) for quick reference during development.

## 1. Programming Conventions

### 1.1 Naming Conventions

**Rule 1.1** - All package names must be lowercase, separated by dots, with each part being a single word.

```
// GOOD
com.alibaba.project.module

// BAD
com.alibaba.project.Module
com.alibaba.project-module
```

**Rule 1.2** - Class names use UpperCamelCase, must be nouns.

```
// GOOD
UserService
OrderController
DataProcessor

// BAD
userService
OrderControllerService
ProcessData
```

**Rule 1.3** - Method names use lowerCamelCase, must be verbs.

```
// GOOD
getUserById()
calculateTotal()
isUserActive()

// BAD
GetUserById()
userById()
UserActive()
```

**Rule 1.4** - Constants use UPPER_SNAKE_CASE, must be final.

```
// GOOD
private static final int MAX_RETRY_COUNT = 3;
private static final String DEFAULT_ENCODING = "UTF-8";

// BAD
private static final int maxRetryCount = 3;
private static final String default_encoding = "UTF-8";
```

**Rule 1.5** - Abstract classes start with `Abstract` or `Base`. Exception classes end with `Exception`. Test classes start with the class name being tested and end with `Test`.

```
// GOOD
AbstractUserService
BaseController
BusinessException
UserServiceTest

// BAD
AbsUserService
Business
UserService
TestUserService
```

**Rule 1.6** - Array type declarations place brackets after the type, not after the variable name.

```
// GOOD
String[] names
int[] ages

// BAD
String names[]
int ages[]
```

**Rule 1.7** - Boolean variables use `is`, `has`, `can`, `should` prefix.

```
// GOOD
boolean isValid
boolean hasPermission
boolean canExecute
boolean shouldRetry

// BAD
boolean valid
boolean permission
boolean execute
```

### 1.2 Code Format

**Rule 1.8** - Use 4 spaces for indentation, no tabs.

**Rule 1.9** - Maximum line length is 120 characters. Use line breaks for longer lines.

**Rule 1.10** - Each statement is on a separate line.

```
// GOOD
int a = 1;
int b = 2;

// BAD
int a = 1; int b = 2;
```

**Rule 1.11** - Braces start on the same line as the declaration.

```
// GOOD
if (condition) {
    doSomething();
}

// BAD
if (condition)
{
    doSomething();
}

if (condition) { doSomething(); }
```

**Rule 1.12** - Maximum 80 lines per method. If longer, extract into smaller methods.

**Rule 1.13** - Maximum 5 parameters per method. If more parameters are needed, use a parameter object (DTO).

```
// GOOD
public void createUser(CreateUserRequest request) { ... }

// BAD
public void createUser(String name, String email, String phone, 
                       String address, String city, String country) { ... }
```

**Rule 1.14** - Avoid magic numbers and magic strings. Use named constants.

```
// GOOD
if (status == OrderStatus.PAID) { ... }
private static final int MAX_RETRY_COUNT = 3;

// BAD
if (status == 2) { ... }
if (retryCount > 3) { ... }
```

### 1.3 OOP Rules

**Rule 1.15** - Avoid using `==` to compare objects. Use `equals()` method.

```
// GOOD
if (user1.equals(user2)) { ... }

// BAD
if (user1 == user2) { ... }
```

**Rule 1.16** - Always override `equals()` when overriding `hashCode()`.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    User user = (User) o;
    return Objects.equals(id, user.id);
}

@Override
public int hashCode() {
    return Objects.hash(id);
}
```

**Rule 1.17** - Override `toString()` method to provide meaningful string representation.

**Rule 1.18** - Use access modifiers appropriately. Prefer private over protected, protected over public.

**Rule 1.19** - Avoid mutable static variables. If needed, use thread-safe patterns.

## 2. Collections and Data Structures

### 2.1 Collection Selection

**Rule 2.1** - Use `ArrayList` for frequent random access. Use `LinkedList` for frequent insert/delete at head/tail.

**Rule 2.2** - Use `HashSet` for fast lookup. Use `TreeSet` when sorted order is needed.

**Rule 2.3** - Use `HashMap` for key-value storage. Use `TreeMap` when sorted keys are needed.

**Rule 2.4** - Specify initial capacity when collection size is known.

```java
// GOOD
Map<String, User> userMap = new HashMap<>(expectedSize);
List<String> names = new ArrayList<>(100);

// BAD
Map<String, User> userMap = new HashMap<>();
```

### 2.2 Safe Usage

**Rule 2.5** - Avoid `ConcurrentModificationException` by using iterators or concurrent collections.

```java
// GOOD
Iterator<User> iterator = users.iterator();
while (iterator.hasNext()) {
    User user = iterator.next();
    if (user.isInactive()) {
        iterator.remove();
    }
}

// BAD
for (User user : users) {
    if (user.isInactive()) {
        users.remove(user); // ConcurrentModificationException
    }
}
```

**Rule 2.6** - Use `ConcurrentHashMap` instead of `Collections.synchronizedMap(new HashMap())`.

**Rule 2.7** - Use `CopyOnWriteArrayList` for read-heavy, write-light scenarios.

### 2.3 Sublist Handling

**Rule 2.8** - Be careful with subList() - it's a view of the original list, not a copy.

```java
// SubList modifications affect the original list
List<String> subList = list.subList(0, 5);
subList.clear(); // This clears elements from the original list!
```

## 3. Exception Handling

### 3.1 Exception Types

**Rule 3.1** - Distinguish between checked and unchecked exceptions appropriately.

- **Checked Exceptions**: Recoverable errors that callers can handle (IOException, SQLException)
- **Unchecked Exceptions**: Programming errors or unrecoverable conditions (NullPointerException, IllegalArgumentException)

**Rule 3.2** - Never swallow exceptions without logging.

```java
// BAD
try {
    doSomething();
} catch (Exception e) {
    // Swallow exception
}

// GOOD
try {
    doSomething();
} catch (Exception e) {
    log.error("Failed to do something", e);
    throw new BusinessException("Operation failed", e);
}
```

**Rule 3.3** - Never catch `Throwable` or `Error`.

```java
// BAD
catch (Throwable t) { ... }

// GOOD
catch (IOException e) { ... }
catch (SQLException e) { ... }
```

### 3.2 Exception Messages

**Rule 3.4** - Provide meaningful exception messages with context.

```java
// GOOD
throw new BusinessException("User not found with id: " + userId, ErrorCode.USER_NOT_FOUND);

// BAD
throw new BusinessException("User not found");
throw new RuntimeException("Error");
```

**Rule 3.5** - Include the original exception when re-throwing or wrapping.

```java
// GOOD
catch (IOException e) {
    throw new BusinessException("Failed to read file", e);
}

// BAD
catch (IOException e) {
    throw new BusinessException("Failed to read file");
}
```

### 3.3 Try-Catch-Finally

**Rule 3.6** - Always use try-with-resources for AutoCloseable objects.

```java
// GOOD
try (Connection conn = dataSource.getConnection();
     PreparedStatement stmt = conn.prepareStatement(sql)) {
    // ...
}

// BAD
Connection conn = null;
try {
    conn = dataSource.getConnection();
    // ...
} finally {
    if (conn != null) {
        conn.close();
    }
}
```

**Rule 3.7** - Never return from finally block.

```java
// BAD
try {
    return 1;
} finally {
    return 2; // This will override the return from try block
}
```

## 4. Concurrent Programming

### 4.1 Thread Safety

**Rule 4.1** - Always use appropriate synchronization for shared mutable state.

**Rule 4.2** - Prefer `java.util.concurrent` classes over manual synchronization.

```java
// GOOD
ConcurrentHashMap<String, User> userMap = new ConcurrentHashMap<>();
AtomicInteger counter = new AtomicInteger(0);

// BAD
Map<String, User> userMap = Collections.synchronizedMap(new HashMap<>());
int counter = 0; // Not thread-safe without synchronization
```

### 4.2 Thread Pools

**Rule 4.3** - Never create threads directly using `new Thread()`.

```java
// BAD
new Thread(() -> doSomething()).start();

// GOOD
ExecutorService executor = Executors.newFixedThreadPool(10);
executor.submit(() -> doSomething());
executor.shutdown();
```

**Rule 4.4** - Always shutdown thread pools when no longer needed.

```java
executor.shutdown();
try {
    if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
        executor.shutdownNow();
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();
}
```

### 4.3 Synchronization

**Rule 4.5** - Use try-finally for explicit lock acquisition.

```java
// GOOD
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();
}

// BAD
lock.lock();
// critical section
lock.unlock(); // If exception occurs, lock is never released
```

**Rule 4.6** - Use `volatile` only for simple visibility guarantees, not for compound actions.

```java
// GOOD - volatile is sufficient here
private volatile boolean running = true;

// BAD - volatile is not sufficient for compound actions
private volatile int counter = 0;
counter++; // This is not atomic! Use AtomicInteger instead
```

### 4.4 Deadlock Prevention

**Rule 4.7** - Acquire locks in consistent order to prevent deadlock.

```java
// GOOD - Always acquire lock1 before lock2
synchronized (lock1) {
    synchronized (lock2) {
        // ...
    }
}

// BAD - Inconsistent lock order can cause deadlock
synchronized (lock1) {
    // ...
}
synchronized (lock2) {
    synchronized (lock1) { // Different order!
        // ...
    }
}
```

## 5. Logging

### 5.1 Logging Levels

**Rule 5.1** - Use appropriate logging levels:

- **ERROR**: System errors that require immediate attention, might need manual intervention
- **WARN**: Potentially harmful situations that don't prevent the application from running
- **INFO**: Important runtime events, significant state changes
- **DEBUG**: Detailed debugging information for troubleshooting
- **TRACE**: Very fine-grained debugging information, more detailed than DEBUG

### 5.2 Logging Best Practices

**Rule 5.2** - Use parameterized logging instead of string concatenation.

```java
// GOOD
logger.info("User login: userId={}, ip={}", userId, ip);

// BAD
logger.info("User login: " + userId + ", ip: " + ip);
```

**Rule 5.3** - Always log exceptions with stack trace.

```java
// GOOD
logger.error("Failed to process order: orderId={}", orderId, exception);

// BAD
logger.error("Failed to process order: " + orderId);
logger.error("Failed to process order", exception); // No context
```

**Rule 5.4** - Never log sensitive information (passwords, tokens, PII).

```java
// BAD
logger.info("User login: username={}, password={}", username, password);

// GOOD
logger.info("User login attempt: username={}", username);
```

**Rule 5.5** - Include traceId/transactionId in log messages for distributed tracing.

```java
logger.info("Processing request: traceId={}, endpoint={}", traceId, endpoint);
```

## 6. Database

### 6.1 SQL Conventions

**Rule 6.1** - Always use parameterized queries to prevent SQL injection.

```java
// GOOD
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement stmt = conn.prepareStatement(sql);
stmt.setLong(1, userId);

// BAD
String sql = "SELECT * FROM users WHERE id = " + userId;
Statement stmt = conn.createStatement();
stmt.executeQuery(sql);
```

**Rule 6.2** - Use appropriate SQL keywords in uppercase.

```java
// GOOD
String sql = "SELECT id, name, email FROM users WHERE status = ?";

// BAD
String sql = "select id, name, email from users where status = ?";
```

### 6.2 Transaction Management

**Rule 6.3** - Keep transactions as short as possible.

**Rule 6.4** - Use appropriate isolation levels based on business requirements.

**Rule 6.5** - Always rollback transaction on exception.

```java
@Transactional
public void transferMoney(Long fromId, Long toId, BigDecimal amount) {
    try {
        // transfer logic
    } catch (Exception e) {
        // Transaction will be rolled back automatically
        throw new BusinessException("Transfer failed", e);
    }
}
```

### 6.3 ORM Best Practices

**Rule 6.6** - Use lazy loading by default, eager loading only when necessary.

```java
@Entity
public class Order {
    @OneToMany(fetch = FetchType.LAZY, mappedBy = "order")
    private List<OrderItem> items;
}
```

**Rule 6.7** - Avoid N+1 query problem using JOIN FETCH or entity graphs.

```java
// GOOD
@Query("SELECT o FROM Order o LEFT JOIN FETCH o.items WHERE o.id = :id")
Order findOrderWithItems(@Param("id") Long id);

// BAD - causes N+1 queries
Order order = orderRepository.findById(orderId);
List<OrderItem> items = order.getItems(); // Additional queries for each order
```

**Rule 6.8** - Use connection pooling (HikariCP, Druid).

```java
// HikariCP configuration example
@Bean
public DataSource dataSource() {
    HikariConfig config = new HikariConfig();
    config.setJdbcUrl(jdbcUrl);
    config.setUsername(username);
    config.setPassword(password);
    config.setMaximumPoolSize(20);
    config.setMinimumIdle(5);
    return new HikariDataSource(config);
}
```

## 7. API Design

### 7.1 RESTful Conventions

**Rule 7.1** - Use appropriate HTTP methods:

- **GET**: Retrieve resources
- **POST**: Create new resources
- **PUT**: Update entire resources
- **PATCH**: Partially update resources
- **DELETE**: Remove resources

**Rule 7.2** - Use plural nouns for resource names.

```
// GOOD
GET /users
GET /users/{id}
POST /users
PUT /users/{id}
DELETE /users/{id}

// BAD
GET /user
GET /getUser
POST /createUser
```

**Rule 7.3** - Return appropriate HTTP status codes:

- **200 OK**: Successful GET/PUT/PATCH
- **201 Created**: Successful POST
- **204 No Content**: Successful DELETE
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

```java
@GetMapping("/users/{id}")
public ResponseEntity<User> getUser(@PathVariable Long id) {
    Optional<User> user = userService.findById(id);
    return user.map(ResponseEntity::ok)
               .orElse(ResponseEntity.notFound().build());
}
```

### 7.2 Request/Response Design

**Rule 7.4** - Separate DTOs from domain entities.

```java
// DTOs
public class UserDTO {
    private Long id;
    private String username;
    private String email;
}

public class CreateUserRequest {
    @NotBlank
    private String username;
    
    @Email
    private String email;
}

// Domain entity
@Entity
public class User {
    @Id
    private Long id;
    private String username;
    private String email;
    // ... other fields and relationships
}
```

**Rule 7.5** - Use validation annotations for request DTOs.

```java
public class CreateUserRequest {
    @NotBlank(message = "Username is required")
    @Size(min = 3, max = 20, message = "Username must be between 3 and 20 characters")
    private String username;
    
    @Email(message = "Invalid email format")
    @NotBlank(message = "Email is required")
    private String email;
    
    @Pattern(regexp = "^\\+?[0-9]{10,15}$", message = "Invalid phone number")
    private String phone;
}
```

### 7.3 Pagination

**Rule 7.6** - Support pagination for list queries.

```java
@GetMapping("/users")
public ResponseEntity<Page<UserDTO>> getUsers(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size) {
    
    Pageable pageable = PageRequest.of(page, size, Sort.by("createdAt").descending());
    Page<UserDTO> users = userService.getUsers(pageable);
    return ResponseEntity.ok(users);
}
```

**Rule 7.7** - Limit maximum page size to prevent performance issues.

```java
if (size > 100) {
    size = 100; // Enforce maximum page size
}
```

### 7.4 Versioning

**Rule 7.8** - Include API version in URL or headers.

```
// URL versioning
GET /api/v1/users
GET /api/v2/users

// Header versioning
GET /api/users
Headers: API-Version: 1
```

## 8. Performance Optimization

### 8.1 String Handling

**Rule 8.1** - Use StringBuilder for string concatenation in loops.

```java
// GOOD
StringBuilder sb = new StringBuilder();
for (String item : items) {
    sb.append(item).append(", ");
}

// BAD - creates many temporary String objects
String result = "";
for (String item : items) {
    result += item + ", ";
}
```

**Rule 8.2** - Simple string concatenation is fine (compiler optimizes).

```java
// OK - compiler converts to StringBuilder
String message = "Hello " + name + ", welcome!";
```

### 8.2 Collection Optimization

**Rule 8.3** - Choose appropriate collection type based on use case.

- **ArrayList**: Fast random access, slow insert/delete
- **LinkedList**: Fast insert/delete, slow random access
- **HashSet**: Fast lookup, no ordering
- **TreeSet**: Fast lookup, sorted order
- **HashMap**: Fast key-value lookup
- **TreeMap**: Fast lookup, sorted keys

**Rule 8.4** - Set initial capacity when size is known.

```java
// GOOD - avoids resizing
List<String> list = new ArrayList<>(expectedSize);
Map<String, User> map = new HashMap<>(expectedSize);

// BAD - may require multiple resizes
List<String> list = new ArrayList<>();
```

### 8.3 Caching

**Rule 8.5** - Use caching for frequently accessed, rarely changed data.

```java
// Using Caffeine cache
@Bean
public Cache<String, User> userCache() {
    return Caffeine.newBuilder()
        .maximumSize(1000)
        .expireAfterWrite(10, TimeUnit.MINUTES)
        .build();
}
```

**Rule 8.6** - Invalidate cache appropriately when data changes.

```java
public void updateUser(User user) {
    userRepository.save(user);
    userCache.invalidate(String.valueOf(user.getId()));
}
```

### 8.4 Lazy Initialization

**Rule 8.7** - Use thread-safe lazy initialization patterns.

```java
// GOOD - Lazy holder idiom for singletons
private static class SingletonHolder {
    private static final Singleton INSTANCE = new Singleton();
}

public static Singleton getInstance() {
    return SingletonHolder.INSTANCE;
}

// GOOD - For specific lazy initialization
private volatile HeavyObject heavyObject;

public HeavyObject getHeavyObject() {
    if (heavyObject == null) {
        synchronized (this) {
            if (heavyObject == null) {
                heavyObject = new HeavyObject();
            }
        }
    }
    return heavyObject;
}
```

## 9. Security

### 9.1 Input Validation

**Rule 9.1** - Validate all user input.

```java
@PostMapping("/users")
public ResponseEntity<?> createUser(@Valid @RequestBody CreateUserRequest request) {
    // If validation fails, returns 400 automatically
    userService.createUser(request);
    return ResponseEntity.ok().build();
}
```

**Rule 9.2** - Sanitize input to prevent XSS attacks.

```java
// Use framework-provided escaping
String safeHtml = Jsoup.clean(userInput, Whitelist.basic());
```

### 9.2 Authentication and Authorization

**Rule 9.3** - Implement proper authentication mechanisms.

```java
// Using Spring Security
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(OAuth2ResourceServerConfigurer::jwt);
        return http.build();
    }
}
```

**Rule 9.4** - Use role-based access control (RBAC).

```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public void deleteUser(@PathVariable Long id) {
    userService.deleteUser(id);
}

@PreAuthorize("@securityService.canAccessUser(#userId)")
@GetMapping("/users/{userId}")
public User getUser(@PathVariable Long userId) {
    return userService.findById(userId);
}
```

### 9.3 Sensitive Data Protection

**Rule 9.5** - Encrypt sensitive data at rest.

```java
// Using AES encryption
public String encrypt(String plaintext) {
    Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
    cipher.init(Cipher.ENCRYPT_MODE, secretKey);
    byte[] encrypted = cipher.doFinal(plaintext.getBytes());
    return Base64.getEncoder().encodeToString(encrypted);
}
```

**Rule 9.6** - Use secure password hashing.

```java
// Using BCrypt
public String hashPassword(String rawPassword) {
    BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
    return encoder.encode(rawPassword);
}

public boolean checkPassword(String rawPassword, String encodedPassword) {
    BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
    return encoder.matches(rawPassword, encodedPassword);
}
```

**Rule 9.7** - Never log sensitive information.

```java
// BAD
logger.info("User login: username={}, password={}", username, password);

// GOOD
logger.info("User login attempt: username={}", username);
```

## 10. Testing

### 10.1 Unit Testing

**Rule 10.1** - Test public interfaces, not implementation details.

**Rule 10.2** - Use descriptive test names.

```java
// GOOD
@Test
public void shouldReturnErrorWhenUserNotFound() {
    // ...
}

// BAD
@Test
public void testUser() {
    // ...
}
```

**Rule 10.3** - Mock external dependencies.

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    public void shouldReturnUserWhenExists() {
        // Given
        User user = new User();
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        
        // When
        User result = userService.getUserById(1L);
        
        // Then
        assertThat(result).isNotNull();
        verify(userRepository).findById(1L);
    }
}
```

### 10.2 Integration Testing

**Rule 10.4** - Use testcontainers for consistent test environments.

```java
@SpringBootTest
@Testcontainers
class UserRepositoryTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:14");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
    }
    
    @Test
    public void shouldSaveUser() {
        // ...
    }
}
```

### 10.3 Test Coverage

**Rule 10.5** - Aim for > 80% code coverage for critical business logic.

**Rule 10.6** - Focus on testing edge cases and error conditions.

```java
@Test
public void shouldHandleNullInput() {
    assertThrows(IllegalArgumentException.class, () -> {
        userService.createUser(null);
    });
}

@Test
public void shouldHandleDuplicateUser() {
    // Test duplicate user scenario
}
```

## Reference

This document is based on the Alibaba Taishan Java Development Manual (泰山版). For the complete manual, refer to the official documentation.
