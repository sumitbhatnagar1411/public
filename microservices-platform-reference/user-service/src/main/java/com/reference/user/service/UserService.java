package com.reference.user.service;

import com.reference.user.domain.User;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;

@Service
public class UserService {

    private final List<User> store = new CopyOnWriteArrayList<>();

    public UserService() {
        store.add(new User("user-1", "alice@example.com", "Alice"));
        store.add(new User("user-2", "bob@example.com", "Bob"));
    }

    public List<User> findAll() {
        return List.copyOf(store);
    }

    public Optional<User> findById(String id) {
        return store.stream().filter(u -> u.id().equals(id)).findFirst();
    }

    @KafkaListener(topics = "order.created", groupId = "user-service")
    public void onOrderCreated(String message) {
        // Example: react to order events (e.g. update analytics, send notification)
        System.out.println("[user-service] Order event: " + message);
    }
}
