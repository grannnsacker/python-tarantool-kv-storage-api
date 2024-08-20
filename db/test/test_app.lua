box.cfg{
    listen = 3302,
}

if box.space.kv_store then
    box.space.kv_store:drop()
end

local kv_store = box.schema.create_space('kv_store', { format = {
    { name = 'key', type = 'scalar' },
    { name = 'value', type = 'scalar' }
}})

kv_store:create_index('pk', {parts = {'key'}, if_not_exists=true })

if box.space.users then
    box.space.users:drop()
end

local users = box.schema.create_space('users', { format = {
    { name = 'username', type = 'string' },
    { name = 'password', type = 'string' }
}})

users:create_index('pk', {parts = {'username'}, if_not_exists=true })

local function add_user_if_not_exists(username, password)
    local user = users:get(username)
    if user == nil then
        users:insert({username, password})
        return true
    end
    return false
end

add_user_if_not_exists('admin', '$2y$12$rYbeEBnXA6IAp5Xib00pCOvTwcPp6rN3qdxf0ioY9HPy6UN1xFiNO')



