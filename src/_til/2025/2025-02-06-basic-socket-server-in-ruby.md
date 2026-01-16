---
layout: til
title: A basic socket server in Ruby
summary: My first bit of socket programming is a Ruby server that reads lines from the socket, and prints them. Not useful on its own, but a stepping stone to more exciting things!
date: 2025-02-06 09:13:10 +00:00
tags:
  - ruby
---
I'm working on a new project that involves sockets, and I decided to try writing a basic socket server in Ruby.
Here's the code I wrote:

```ruby
require 'socket'

class SocketServer

  # Opens a server listening to `port` and returns a new
  # `TCPServer` object.
  #
  #     SocketServer.open(port) do |server|
  #       loop do
  #         client = server.accept
  #         … do stuff with client connection
  #       end
  #     end
  #
  # The server will automatically be shut down when the block completes.
  def self.open(port)
    server = TCPServer.new(port)

    begin
      yield(server)
    rescue Interrupt
      puts "\nShutting down server..."
    ensure
      server.close
      puts "Server shut down"
    end
  end

  # Manages a client connection on a socket.
  #
  #     client = server.accept
  #
  #     SocketServer.handle_client(client) do |connection|
  #       while line = connection.gets
  #         puts "Received #{line}
  #         … do other stuff with connection
  #       end
  #     end
  #
  # The connection will automatically be closed and cleaned up
  # when the block completes.
  def self.handle_client(client)
    puts "New client connected from: #{client.remote_address.ip_address}"

    begin
      yield(client)
    rescue Errno::ECONNRESET
      puts "Client disconnected unexpectedly"
    ensure
      client.close
      puts "Client disconnected"
    end
  end
end

SocketServer.open(port = 3000) do |server|
  loop do
    client = server.accept

    SocketServer.handle_client(client) do |connection|
      while line = connection.gets
        line.chomp!
        puts "Received: #{line}"
        connection.puts "Received: #{line}"
      end
    end
  end
end
```

Run it as:

```console
$ ruby server.rb
```

You can send lines to the server with `nc`:

```console
$ echo 'Hello world!' | nc localhost 3000
```

The server will print the messages sent to the socket, for example:

```
New client connected from: ::1
Received: Hello world!
Client disconnected
```

As well as my first time doing socket programming, this is the first time I've used Ruby's `begin … rescue … ensure` blocks, which feel analogous to context managers in Python.
Here's [a Stack Overflow answer](https://stackoverflow.com/a/3875832/1558022) by Jörg W Mittag which helped me understand what's going on here.
