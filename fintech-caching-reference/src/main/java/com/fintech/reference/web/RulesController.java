package com.fintech.reference.web;

import com.fintech.reference.rules.RuleEngine;
import com.fintech.reference.rules.RuleResult;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/rules")
public class RulesController {

    private final RuleEngine ruleEngine;

    public RulesController(RuleEngine ruleEngine) {
        this.ruleEngine = ruleEngine;
    }

    @PostMapping("/evaluate")
    public List<RuleResult> evaluate(@RequestBody Map<String, Object> context) {
        return ruleEngine.evaluate(context);
    }
}
