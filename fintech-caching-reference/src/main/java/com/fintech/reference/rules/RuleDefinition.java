package com.fintech.reference.rules;

import java.util.List;
import java.util.Map;

public record RuleDefinition(
    String id,
    String name,
    List<Map<String, Object>> conditions,
    Map<String, Object> action
) {}
