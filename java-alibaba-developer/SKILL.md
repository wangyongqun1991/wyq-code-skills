---
name: java-alibaba-developer
description: This skill should be used whenever the user requests Java development work, code review, or system design tasks. It provides comprehensive guidance following Alibaba Taishan Java Development Manual (泰山版) standards, including naming conventions, exception handling, code structure, concurrency practices, logging standards, and database best practices.
---

# Java Alibaba Developer

## Overview

This skill enables professional-grade Java development following Alibaba Taishan Java Development Manual standards. It provides comprehensive guidance on naming conventions, code structure, exception handling, concurrent programming, logging, database operations, and system design principles. Use this skill for all Java development, code review, refactoring, and system design tasks to ensure code quality, maintainability, and production readiness.

## When to Use This Skill

Invoke this skill when:
- Writing or reviewing Java code for production systems
- Designing or refactoring Java applications
- Implementing concurrent or multi-threaded features
- Setting up logging and monitoring infrastructure
- Designing database interactions and ORM mappings
- Conducting code reviews or quality assessments
- Creating technical specifications or coding standards documentation

## Core Development Standards

### Naming Conventions

Follow these naming rules strictly:

1. **Package Names**
   - Use lowercase, reverse domain naming
   - Maximum 3 levels deep for most cases
   - Example: `com.alibaba.project.module`

2. **Class Names**
   - Use UpperCamelCase (PascalCase)
   - Noun-based, descriptive names
   - Example: `UserService`, `OrderController`, `DataProcessor`

3. **Method Names**
   - Use lowerCamelCase
   - Verb-based for actions, is/has for booleans
   - Example: `getUserById()`, `isUserActive()`, `calculateTotal()`

4. **Variable Names**
   - Use lowerCamelCase
   - Avoid abbreviations unless universally understood
   - Example: `userName` (not `un`), `orderTotal` (not `ot`)

5. **Constants**
   - Use UPPER_SNAKE_CASE
   - Place in dedicated constants classes or enums
   - Example: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`

6. **Boolean Variables**
   - Prefix with `is`, `has`, `can`, `should`
   - Example: `isValid`, `hasPermission`, `canExecute`

### Code Structure and Organization

1. **File Layout** (in order):
   ```java
   // 1. License header
   // 2. Package statement
   // 3. Imports (grouped: standard, third-party, custom)
   // 4. Class documentation
   // 5. Class declaration
   // 6. Constants
   // 7. Static variables
   // 8. Instance variables
   // 9. Constructors
   // 10. Static methods
   // 11. Instance methods
   // 12. Inner classes
   ```

2. **Import Organization**:
   - Group imports: standard library, third-party, internal packages
   - Remove unused imports
   - Use wildcard imports only for static imports of constants

3. **Method Length**:
   - Maximum 80 lines per method
   - If longer, extract into smaller methods

4. **Parameter Count**:
   - Maximum 5 parameters
   - For more parameters, use parameter objects (DTOs)

### Exception Handling

1. **Exception Hierarchy**:
   ```java
   // Custom exceptions should extend appropriate parent
   public class BusinessException extends RuntimeException {
       private final ErrorCode errorCode;
       // ...
   }
   ```

2. **Try-Catch Blocks**:
   - Catch specific exceptions, not `Exception` or `Throwable`
   - Never swallow exceptions without logging
   - Always provide meaningful error messages

3. **Throw Statements**:
   ```java
   // GOOD: Provide context
   throw new BusinessException("User not found", ErrorCode.USER_NOT_FOUND);

   // BAD: Generic message
   throw new RuntimeException("Error occurred");
   ```

4. **Finally Blocks**:
   - Ensure resource cleanup
   - Prefer try-with-resources for AutoCloseable objects
   ```java
   try (Connection conn = dataSource.getConnection();
        PreparedStatement stmt = conn.prepareStatement(sql)) {
       // ...
   }
   ```

### Concurrent Programming

1. **Thread Safety**:
   - Always use appropriate synchronization mechanisms
   - Prefer `java.util.concurrent` classes over manual synchronization
   - Example: `ConcurrentHashMap` over `Collections.synchronizedMap`

2. **Lock Usage**:
   ```java
   // GOOD: Use try-finally for explicit locks
   lock.lock();
   try {
       // critical section
   } finally {
       lock.unlock();
   }
   ```

3. **Thread Pools**:
   - Never create threads directly with `new Thread()`
   - Use `ExecutorService` with appropriate thread pool
   - Always shutdown thread pools when no longer needed

4. **Volatile Usage**:
   - Use `volatile` only for simple visibility guarantees
   - For compound actions, use proper locking or atomic classes

5. **Atomic Classes**:
   - Prefer `AtomicInteger`, `AtomicLong` for counters
   - Avoid `volatile` for primitive operations

### Logging Standards

1. **Logging Levels**:
   - ERROR: System errors requiring intervention
   - WARN: Potentially harmful situations
   - INFO: Important runtime events
   - DEBUG: Detailed debugging information
   - TRACE: Very fine-grained debugging

2. **Logging Best Practices**:
   ```java
   // GOOD: Structured logging with context
   logger.info("User login succeeded: userId={}, ip={}", userId, ip);

   // BAD: String concatenation
   logger.info("User login succeeded: " + userId + " from " + ip);

   // GOOD: Include error details
   logger.error("Failed to process order: orderId={}", orderId, exception);

   // BAD: No exception information
   logger.error("Failed to process order");
   ```

3. **Conditional Logging**:
   ```java
   // Use parameterized logging instead of string concatenation
   if (logger.isDebugEnabled()) {
       logger.debug("Processing request: {}", request);
   }
   ```

4. **Log Content**:
   - Never log passwords, tokens, or sensitive data
   - Include traceId/transactionId for distributed tracing
   - Use structured logging for log parsing

### Database Operations

1. **SQL Conventions**:
   - Use parameterized queries to prevent SQL injection
   - Never concatenate SQL strings with user input
   - Use prepared statements

2. **Transaction Management**:
   - Keep transactions short and focused
   - Use appropriate isolation levels
   - Always rollback on exceptions

3. **ORM Best Practices**:
   ```java
   // GOOD: Lazy loading with appropriate fetching
   @Entity
   @Table(name = "users")
   @NamedEntityGraph(name = "User.withRoles", attributeNodes = @NamedAttributeNode("roles"))
   public class User {
       @OneToMany(fetch = FetchType.LAZY, mappedBy = "user")
       private Set<Role> roles;
   }

   // Avoid N+1 queries with JOIN FETCH or entity graphs
   ```

4. **Connection Pooling**:
   - Use connection pools (HikariCP, Druid)
   - Configure appropriate pool size based on workload
   - Monitor connection pool metrics

5. **Index Usage**:
   - Create indexes on frequently queried columns
   - Avoid indexes on columns with low cardinality
   - Use composite indexes for multi-column queries

### API Design

1. **RESTful Conventions**:
   - Use appropriate HTTP methods (GET, POST, PUT, DELETE)
   - Use plural nouns for resource names
   - Return appropriate status codes
   ```java
   // GOOD: RESTful design
   @GetMapping("/users/{id}")
   public ResponseEntity<User> getUser(@PathVariable Long id) {
       User user = userService.findById(id);
       return ResponseEntity.ok(user);
   }
   ```

2. **Request/Response DTOs**:
   - Separate DTOs from domain entities
   - Use validation annotations
   ```java
   public class CreateUserRequest {
       @NotBlank(message = "Username is required")
       @Size(min = 3, max = 20)
       private String username;

       @Email(message = "Invalid email format")
       private String email;
   }
   ```

3. **Pagination**:
   - Support pagination for list queries
   - Use page and size parameters
   ```java
   @GetMapping("/users")
   public ResponseEntity<Page<UserDTO>> getUsers(
           @RequestParam(defaultValue = "0") int page,
           @RequestParam(defaultValue = "20") int size) {
       Page<UserDTO> users = userService.getUsers(page, size);
       return ResponseEntity.ok(users);
   }
   ```

4. **Versioning**:
   - Include API version in URL or headers
   - Maintain backward compatibility when possible

### Performance Optimization

1. **String Handling**:
   - Use `StringBuilder` for string concatenation in loops
   - String concatenation is fine for simple cases (compiler optimizes)

2. **Collection Usage**:
   - Choose appropriate collection type based on use case
   - Set initial capacity when size is known
   ```java
   // GOOD: Pre-size collection
   Map<String, User> userMap = new HashMap<>(expectedSize);
   ```

3. **Caching**:
   - Use caching for frequently accessed data
   - Consider caching strategies (LRU, time-based)
   - Invalidate cache appropriately

4. **Lazy Initialization**:
   ```java
   // GOOD: Lazy holder pattern for singleton
   private static class SingletonHolder {
       private static final Singleton INSTANCE = new Singleton();
   }

   public static Singleton getInstance() {
       return SingletonHolder.INSTANCE;
   }
   ```

### Code Review Checklist

Before considering code complete, verify:

- [ ] Naming follows conventions (camelCase, PascalCase, UPPER_SNAKE_CASE)
- [ ] Methods are <= 80 lines, classes <= 2000 lines
- [ ] Parameters are <= 5, use DTOs if more
- [ ] All exceptions are caught appropriately and logged
- [ ] No resource leaks (use try-with-resources)
- [ ] Thread-safe when needed (concurrent classes, proper synchronization)
- [ ] Logging is appropriate and includes context
- [ ] SQL queries use parameterized statements
- [ ] Transactions are properly scoped
- [ ] API methods return proper status codes
- [ ] Input validation is in place
- [ ] Sensitive data is not logged
- [ ] Comments are concise and explain "why" not "what"
- [ ] No dead code or commented-out code
- [ ] Proper error handling at boundaries (API, database)

## Common Anti-Patterns to Avoid

1. **Magic Numbers**:
   ```java
   // BAD
   if (status == 1) { ... }

   // GOOD
   if (status == Status.ACTIVE) { ... }
   ```

2. **Deep Nesting**:
   ```java
   // BAD: Too nested
   if (condition1) {
       if (condition2) {
           if (condition3) {
               doSomething();
           }
       }
   }

   // GOOD: Early return
   if (!condition1 || !condition2 || !condition3) {
       return;
   }
   doSomething();
   ```

3. **Overly General Exceptions**:
   ```java
   // BAD
   catch (Exception e) { ... }

   // GOOD
   catch (IOException e) { ... }
   catch (SQLException e) { ... }
   ```

4. **Unnecessary Synchronization**:
   - Only synchronize when truly needed
   - Prefer fine-grained locks over coarse-grained

5. **Hard-coded Configuration**:
   - Externalize configuration
   - Use configuration management tools

## Documentation Standards

1. **JavaDoc**:
   ```java
   /**
    * Validates user credentials and returns authentication token.
    *
    * @param username the username to validate
    * @param password the password to validate (will be hashed)
    * @return authentication token if credentials are valid
    * @throws AuthenticationException if credentials are invalid
    * @throws UserServiceUnavailableException if user service is down
    */
   public String authenticate(String username, String password) {
       // ...
   }
   ```

2. **Inline Comments**:
   - Comment "why", not "what"
   - Keep comments up-to-date
   - Remove obsolete comments

3. **Class Documentation**:
   - Explain the purpose and responsibilities
   - Document usage examples for complex classes

## Testing Standards

1. **Unit Testing**:
   - Test public interfaces, not implementation details
   - Use meaningful test names: `shouldReturnErrorWhenUserNotFound`
   - Mock external dependencies
   ```java
   @Test
   public void shouldReturnErrorWhenUserNotFound() {
       when(userRepository.findById(1L)).thenReturn(Optional.empty());

       assertThrows(UserNotFoundException.class,
           () -> userService.getUserById(1L));
   }
   ```

2. **Integration Testing**:
   - Test database interactions
   - Test API endpoints
   - Use testcontainers for consistent test environments

3. **Test Coverage**:
   - Aim for > 80% code coverage for critical business logic
   - Focus on testing edge cases and error conditions

## Security Considerations

1. **Input Validation**:
   - Validate all user input
   - Use framework validators where possible

2. **Output Encoding**:
   - Encode output to prevent XSS attacks
   - Use framework-provided escaping

3. **Authentication/Authorization**:
   - Implement proper authentication mechanisms
   - Use role-based access control (RBAC)
   - Validate permissions at each layer

4. **Sensitive Data**:
   - Encrypt sensitive data at rest and in transit
   - Never log passwords, tokens, or PII
   - Use secure password hashing (bcrypt, Argon2)

## Performance Monitoring

1. **Metrics**:
   - Monitor key metrics: response time, error rate, throughput
   - Use APM tools (SkyWalking, Pinpoint)

2. **Alerting**:
   - Set up alerts for critical failures
   - Monitor resource usage (CPU, memory, disk)

3. **Profiling**:
   - Profile code to identify bottlenecks
   - Use async processing for long-running tasks

## Resources

This skill includes reference materials to support Java development following Alibaba standards:

### references/
Contains detailed reference documentation:
- `alibaba_taishan_standards.md` - Detailed Alibaba Taishan manual excerpts
- `code_templates.md` - Common code templates and patterns
- `best_practices.md` - Additional best practices and anti-patterns

Load these reference documents when detailed specifications or examples are needed for specific tasks.

---
