package com.fintech.reference.web;

import com.fintech.reference.rules.RuleEngine;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
@RequestMapping("/api/admin")
public class AdminController {

    private final RuleEngine ruleEngine;

    public AdminController(RuleEngine ruleEngine) {
        this.ruleEngine = ruleEngine;
    }

    @PostMapping("/rules/reload")
    public ResponseEntity<String> reloadRules() {
        try {
            ruleEngine.reloadRules();
            return ResponseEntity.ok("Rules reloaded");
        } catch (IOException e) {
            return ResponseEntity.internalServerError().body("Reload failed: " + e.getMessage());
        }
    }
}
