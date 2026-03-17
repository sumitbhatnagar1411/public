package com.reference.order.domain;

import java.time.Instant;

public record Order(String id, String userId, String productId, int quantity, String status, Instant createdAt) {}
