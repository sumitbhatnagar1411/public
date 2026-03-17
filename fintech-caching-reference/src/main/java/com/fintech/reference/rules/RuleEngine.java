package com.fintech.reference.rules;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class RuleEngine {

    private static final Logger log = LoggerFactory.getLogger(RuleEngine.class);
    private final ObjectMapper mapper = new ObjectMapper();
    private final List<RuleDefinition> rules = new CopyOnWriteArrayList<>();

    @PostConstruct
    public void loadRules() throws IOException {
        reloadRules();
    }

    public void reloadRules() throws IOException {
        rules.clear();
        PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
        Resource[] resources = resolver.getResources("classpath:rules/*.json");
        for (Resource r : resources) {
            try (InputStream is = r.getInputStream()) {
                List<RuleDefinition> list = mapper.readValue(is, new TypeReference<>() {});
                rules.addAll(list);
                log.info("Loaded {} rules from {}", list.size(), r.getFilename());
            }
        }
    }

    public List<RuleResult> evaluate(Map<String, Object> context) {
        List<RuleResult> results = new ArrayList<>();
        for (RuleDefinition rule : rules) {
            boolean match = true;
            for (Map<String, Object> cond : rule.conditions()) {
                if (!evaluateCondition(cond, context)) {
                    match = false;
                    break;
                }
            }
            results.add(new RuleResult(rule.id(), rule.name(), match, match ? rule.action() : null));
        }
        return results;
    }

    @SuppressWarnings("unchecked")
    private boolean evaluateCondition(Map<String, Object> cond, Map<String, Object> context) {
        String field = (String) cond.get("field");
        String op = (String) cond.get("op");
        Object expected = cond.get("value");
        Object actual = getByPath(context, field);
        if (actual == null) return "null".equals(op) || "absent".equals(op);
        return switch (op) {
            case "eq" -> actual.equals(expected);
            case "neq" -> !actual.equals(expected);
            case "gt" -> compare(actual, expected) > 0;
            case "gte" -> compare(actual, expected) >= 0;
            case "lt" -> compare(actual, expected) < 0;
            case "lte" -> compare(actual, expected) <= 0;
            case "in" -> ((List<?>) expected).contains(actual);
            default -> false;
        };
    }

    private Object getByPath(Map<String, Object> map, String path) {
        Object current = map;
        for (String key : path.split("\\.")) {
            if (current instanceof Map) {
                current = ((Map<?, ?>) current).get(key);
            } else {
                return null;
            }
        }
        return current;
    }

    private int compare(Object a, Object b) {
        if (a instanceof Number na && b instanceof Number nb) {
            return Double.compare(na.doubleValue(), nb.doubleValue());
        }
        return String.valueOf(a).compareTo(String.valueOf(b));
    }

    public record RuleResult(String ruleId, String ruleName, boolean matched, Map<String, Object> action) {}
}
