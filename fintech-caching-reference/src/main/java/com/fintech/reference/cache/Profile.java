package com.fintech.reference.cache;

import java.time.Instant;

public record Profile(String id, String customerId, String segment, String region, boolean active, Instant updatedAt) {}
