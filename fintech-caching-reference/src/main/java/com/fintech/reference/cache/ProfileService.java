package com.fintech.reference.cache;

import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class ProfileService {

    private final Map<String, Profile> store = new ConcurrentHashMap<>();

    public ProfileService() {
        store.put("profile-1", new Profile("profile-1", "C1", "premium", "US", true, Instant.now()));
        store.put("profile-2", new Profile("profile-2", "C2", "standard", "US", true, Instant.now()));
        store.put("profile-3", new Profile("profile-3", "C3", "premium", "EU", true, Instant.now()));
    }

    @Cacheable(value = CacheConfig.PROFILE_CACHE, key = "#id")
    public Optional<Profile> getById(String id) {
        return Optional.ofNullable(store.get(id));
    }
}
